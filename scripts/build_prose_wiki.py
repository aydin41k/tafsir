#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editorial_style import normalize_sentence_initial_ayah_ordinals  # noqa: E402
from pipeline import ROOT, call_azure, local_rest, row_range  # noqa: E402

VAULT = ROOT / "vault"
STAGING = ROOT / "vault-next"
ARCHIVE = ROOT / "archive"
CACHE = ROOT / "data/prose"
PILOT_CACHE = ROOT / "data/prose-pilot"
PROMPT = (ROOT / "prompts/transcript-to-prose.md").read_text(encoding="utf-8")
SURAHS = {
    "ali-imran": {"key": "ali-imran", "name": "Âl-i İmrân", "stem": "Ali Imran", "number": 3, "ayah_count": 200, "mark": "٣", "allowed_missing_ayahs": [1, 2]},
    "nisa": {"key": "nisa", "name": "Nisâ", "stem": "Nisa", "number": 4, "ayah_count": 176, "mark": "٤", "allowed_missing_ayahs": []},
    "maide": {"key": "maide", "name": "Mâide", "stem": "Maide", "number": 5, "ayah_count": 120, "mark": "٥", "allowed_missing_ayahs": []},
    "enam": {"key": "enam", "name": "En‘âm", "stem": "Enam", "number": 6, "ayah_count": 165, "mark": "٦", "allowed_missing_ayahs": []},
    "araf": {"key": "araf", "name": "A‘râf", "stem": "Araf", "number": 7, "ayah_count": 206},
}


def article_stem(row: dict) -> str:
    return f"{row['id']:03d} - {Path(row['file_name']).stem}"


def raw_stem(row: dict) -> str:
    return f"Ham - {article_stem(row)}"


def row_bounds(row: dict) -> tuple[int, int]:
    return int(row["_ayah_start"]), int(row["_ayah_end"])


def row_surah(row: dict) -> dict:
    return SURAHS[row["_surah_key"]]


def safe(value) -> str:
    return str(value or "").strip()


def frontmatter(title: str, kind: str, **extra) -> str:
    data = {
        "title": title,
        "type": kind,
        "review_status": "machine-edited",
        "editorial_level": "light",
        **extra,
    }
    lines = ["---"]
    for key, value in data.items():
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif isinstance(value, (int, float)):
            rendered = str(value)
        else:
            rendered = json.dumps(str(value), ensure_ascii=False)
        lines.append(f"{key}: {rendered}")
    return "\n".join(lines + ["---", ""])


def write(relative: str, content: str) -> None:
    path = STAGING / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def load_rows() -> tuple[list[dict], dict[int, dict]]:
    rest = local_rest()
    all_rows = rest.get("media_transcriptions", "select=*&type=eq.youtube&order=id.asc")
    sources = rest.get("media_sources", "select=*&order=id.asc")
    source_by_row = {
        source["media_transcription_id"]: source
        for source in sources if source.get("media_transcription_id")
    }
    rows = []
    for row in all_rows:
        source = source_by_row.get(row["id"]) or {}
        key = row.get("surah_key") or source.get("surah_key")
        fallback = row_range(row)
        if not key and fallback:
            key = "araf"
        if key not in SURAHS:
            continue
        start = source.get("ayah_start")
        end = source.get("ayah_end")
        if not start and fallback:
            start, end = fallback
        if not start:
            continue
        row["_surah_key"] = key
        row["_ayah_start"] = int(start)
        row["_ayah_end"] = int(end or start)
        rows.append(row)
    return rows, source_by_row


def split_transcript(text: str, max_chars: int = 8500) -> list[str]:
    chunks = []
    remaining = text.strip()
    while len(remaining) > max_chars:
        cut = remaining.rfind(". ", 0, max_chars)
        if cut < max_chars // 2:
            cut = remaining.rfind("? ", 0, max_chars)
        if cut < max_chars // 2:
            cut = remaining.rfind(" ", 0, max_chars)
        if cut < max_chars // 2:
            cut = max_chars
        else:
            cut += 1
        chunks.append(remaining[:cut].strip())
        remaining = remaining[cut:].strip()
    if remaining:
        chunks.append(remaining)
    return chunks


def edit_transcript_part(row: dict, source_title: str, text: str, part: int, total: int) -> dict:
    surah = row_surah(row)
    message = (
        f"SOURCE TITLE: {source_title}\n"
        f"SOURCE FILE: {row['file_name']}\n"
        f"AYAH RANGE: {surah['name']} {row_bounds(row)}\n"
        f"CONTIGUOUS TRANSCRIPT PART: {part}/{total}\n\n"
        "Edit only this contiguous part. Preserve its opening and ending so it can be joined "
        "directly to the adjacent edited parts. Do not add a part summary or conclusion.\n\n"
        f"RAW TRANSCRIPT PART:\n{text}"
    )
    return call_azure(PROMPT, message, max_tokens=8000, model="gpt-5.4")


def model_call(row: dict, source: dict | None) -> dict:
    transcript = safe(row.get("transcription"))
    source_title = (source or {}).get("title") or Path(row["file_name"]).stem
    surah = row_surah(row)
    if len(transcript) > 16000:
        chunks = split_transcript(transcript)
        parts = [edit_transcript_part(row, source_title, chunk, index, len(chunks)) for index, chunk in enumerate(chunks, start=1)]
        article = normalize_sentence_initial_ayah_ordinals(
            "\n\n".join(safe(part.get("article_markdown")) for part in parts).strip()
        )
        result = {
            "title": source_title,
            "article_markdown": article,
            "editorial_changes": list(dict.fromkeys(
                safe(item) for part in parts for item in (part.get("editorial_changes") or []) if safe(item)
            )),
            "uncertainties": list(dict.fromkeys(
                safe(item) for part in parts for item in (part.get("uncertainties") or []) if safe(item)
            )),
        }
        ratio = len(article) / max(1, len(transcript))
        result.update({
            "row_id": row["id"],
            "raw_characters": len(transcript),
            "article_characters": len(article),
            "retention_ratio": round(ratio, 3),
        })
        return result
    message = (
        f"SOURCE TITLE: {source_title}\n"
        f"SOURCE FILE: {row['file_name']}\n"
        f"AYAH RANGE: {surah['name']} {row_bounds(row)}\n\n"
        f"RAW TRANSCRIPT:\n{transcript}"
    )
    result = call_azure(PROMPT, message, max_tokens=14000, model="gpt-5.4")
    article = normalize_sentence_initial_ayah_ordinals(safe(result.get("article_markdown")))
    ratio = len(article) / max(1, len(transcript))
    if ratio < 0.62:
        result = call_azure(
            PROMPT,
            message + (
                "\n\nRETRY REQUIREMENT: The prior result compressed the source too much. "
                "Retain all substantive detail and stay close to the transcript's length."
            ),
            max_tokens=16000,
            model="gpt-5.4",
        )
        article = normalize_sentence_initial_ayah_ordinals(safe(result.get("article_markdown")))
        ratio = len(article) / max(1, len(transcript))
    result["article_markdown"] = article
    result.update({
        "row_id": row["id"],
        "raw_characters": len(transcript),
        "article_characters": len(article),
        "retention_ratio": round(ratio, 3),
    })
    return result


def convert(row: dict, source: dict | None) -> tuple[int, dict, bool]:
    target = CACHE / f"{row['id']}.json"
    if target.exists():
        return row["id"], json.loads(target.read_text(encoding="utf-8")), True
    pilot = PILOT_CACHE / f"{row['id']}.json"
    if pilot.exists():
        result = json.loads(pilot.read_text(encoding="utf-8"))
        CACHE.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return row["id"], result, True
    last_error = None
    for attempt in range(1, 4):
        try:
            result = model_call(row, source)
            CACHE.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            return row["id"], result, False
        except Exception as exc:
            last_error = exc
            if attempt < 3:
                time.sleep(attempt * 3)
    if "HTTP Error 400" in str(last_error):
        transcript = re.sub(r"\s+", " ", safe(row.get("transcription")))
        sentences = re.split(r"(?<=[.!?])\s+", transcript)
        paragraphs = [" ".join(sentences[index:index + 4]) for index in range(0, len(sentences), 4)]
        article = "\n\n".join(paragraph.strip() for paragraph in paragraphs if paragraph.strip())
        result = {
            "title": (source or {}).get("title") or Path(row["file_name"]).stem,
            "article_markdown": article,
            "editorial_changes": ["Kaynak transkript anlamı değiştirilmeden paragraflara ayrıldı."],
            "uncertainties": ["İçerik filtresi nedeniyle otomatik dil düzenlemesi uygulanmadı; kaynak metin korunmuştur."],
            "row_id": row["id"],
            "raw_characters": len(transcript),
            "article_characters": len(article),
            "retention_ratio": round(len(article) / max(1, len(transcript)), 3),
        }
        CACHE.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return row["id"], result, False
    raise RuntimeError(f"Failed row {row['id']} after retries: {last_error}")


def build_article(row: dict, source: dict | None, result: dict) -> str:
    bounds = row_bounds(row)
    surah = row_surah(row)
    title = safe(result.get("title")) or Path(row["file_name"]).stem
    article = normalize_sentence_initial_ayah_ordinals(safe(result.get("article_markdown")))
    source_title = (source or {}).get("title") or Path(row["file_name"]).stem
    source_url = (source or {}).get("source_url")
    metadata = (source or {}).get("metadata") or {}
    if isinstance(metadata, str):
        try:
            metadata = json.loads(metadata)
        except json.JSONDecodeError:
            metadata = {}
    lines = [
        frontmatter(
            title,
            "tefsir-text",
            row_id=row["id"],
            surah_key=surah["key"],
            surah=surah["name"],
            surah_number=surah["number"],
            ayah_start=bounds[0],
            ayah_end=bounds[1],
            retention_ratio=result.get("retention_ratio", 0),
        ),
        f"# {title}",
        "",
        "> [!info] Editoryal seviye: hafif",
        "> Bu metin kaynak videonun transkriptidir. Yalnızca konuşma dilinden yazı diline geçirilmiş; yeni açıklama, özet veya haricî bilgi eklenmemiştir.",
        "",
        "## Kaynak bilgisi",
        "",
        f"- Video başlığı: {source_title}",
        f"- Kayıt: `{row['file_name']}`",
        f"- Ayet aralığı: {surah['name']} {bounds[0]}" + (f"–{bounds[1]}" if bounds[1] != bounds[0] else ""),
        f"- Ham transkript: [[{raw_stem(row)}]]",
    ]
    if source_url:
        lines.append(f"- Video: {source_url}")
    if metadata.get("transcript_origin"):
        lines.append(f"- Transkript kaynağı: `{metadata['transcript_origin']}`")
    lines.extend(["", "---", "", article])
    uncertainties = [normalize_sentence_initial_ayah_ordinals(safe(item)) for item in result.get("uncertainties") or [] if safe(item)]
    changes = [normalize_sentence_initial_ayah_ordinals(safe(item)) for item in result.get("editorial_changes") or [] if safe(item)]
    lines.extend(["", "---", "", "<details>", "<summary>Editoryal kayıt ve insan kontrolü</summary>", ""])
    lines.extend(["### Uygulanan işlemler", ""] + ([f"- {item}" for item in changes] or ["- Konuşma dili yazı diline geçirildi."]))
    lines.extend(["", "### Kontrol gereken noktalar", ""] + ([f"- {item}" for item in uncertainties] or ["- Model özel bir belirsizlik işaretlemedi."]))
    lines.extend(["", "</details>"])
    return "\n".join(lines)


def build_raw(row: dict, source: dict | None) -> str:
    bounds = row_bounds(row)
    surah = row_surah(row)
    source_title = (source or {}).get("title") or Path(row["file_name"]).stem
    source_url = (source or {}).get("source_url")
    lines = [
        frontmatter(
            f"Ham Transkript — {source_title}",
            "raw-transcript",
            row_id=row["id"],
            surah_key=surah["key"],
            surah=surah["name"],
            surah_number=surah["number"],
            ayah_start=bounds[0],
            ayah_end=bounds[1],
        ),
        f"# Ham Transkript — {source_title}",
        "",
        "> [!warning] Değiştirilmemiş kaynak",
        "> Bu sayfa yerel `media_transcriptions` tablosundaki metni aynen korur.",
        "",
        f"Yazılı sürüm: [[{article_stem(row)}]]",
    ]
    if source_url:
        lines.append(f"Video: {source_url}")
    lines.extend(["", "---", "", safe(row.get("transcription"))])
    return "\n".join(lines)


def preferred_rows(rows: list[dict], ayah: int) -> list[dict]:
    covering = []
    for row in rows:
        start, end = row_bounds(row)
        if start <= ayah <= end:
            covering.append(row)
    if not covering:
        return []
    minimum_span = min((row_bounds(row)[1] - row_bounds(row)[0]) for row in covering)
    return [row for row in covering if row_bounds(row)[1] - row_bounds(row)[0] == minimum_span]


def build_vault(rows: list[dict], source_by_row: dict[int, dict], results: dict[int, dict]) -> None:
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)

    for row in rows:
        write(f"Tefsir-Metinleri/{article_stem(row)}.md", build_article(row, source_by_row.get(row["id"]), results[row["id"]]))
        write(f"Ham-Transkriptler/{raw_stem(row)}.md", build_raw(row, source_by_row.get(row["id"])))

    rows_by_surah = {
        key: [row for row in rows if row["_surah_key"] == key]
        for key in SURAHS
    }
    for key, surah in SURAHS.items():
        surah_rows = rows_by_surah[key]
        for ayah in range(1, surah["ayah_count"] + 1):
            chosen = preferred_rows(surah_rows, ayah)
            lines = [
                frontmatter(
                    f"{surah['name']} {ayah}",
                    "ayah",
                    surah_key=key,
                    surah=surah["name"],
                    surah_number=surah["number"],
                    ayah=ayah,
                    source_count=len(chosen),
                ),
                f"# {surah['name']} {ayah}",
                "",
            ]
            if chosen:
                lines.extend([
                    "> [!info] Kaynak metin",
                    "> Aşağıdaki içerik, bu ayeti kapsayan en dar aralıklı video transkriptlerinden yazı diline geçirilmiştir.",
                ])
            else:
                lines.extend([
                    "> [!warning] Kanal kaynağı bulunamadı",
                    "> 180 Saniyede Tefsir kanalında bu ayeti kapsayan başlıklı bir kaynak video tespit edilemedi. Sayfa, sûre bütünlüğünü korumak için yer tutucu olarak bırakılmıştır.",
                ])
            for row in chosen:
                bounds = row_bounds(row)
                label = f"{surah['name']} {bounds[0]}" + (f"–{bounds[1]}" if bounds[1] != bounds[0] else "")
                lines.extend(["", f"## {label}", "", f"![[{article_stem(row)}]]"])
            previous_link = f"[[{surah['stem']} {ayah - 1:03d}|← {ayah - 1}]]" if ayah > 1 else ""
            next_link = f"[[{surah['stem']} {ayah + 1:03d}|{ayah + 1} →]]" if ayah < surah["ayah_count"] else ""
            lines.extend(["", "---", "", f"{previous_link}  {next_link}".strip()])
            write(f"Ayetler/{surah['stem']}/{surah['stem']} {ayah:03d}.md", "\n".join(lines))

        surah_page = [
            frontmatter(
                surah["name"], "surah", surah_key=key, surah_number=surah["number"],
                ayah_count=surah["ayah_count"], source_count=len(surah_rows),
            ),
            f"# {surah['name']}", "", "## Ayet haritası", "",
        ]
        for start in range(1, surah["ayah_count"] + 1, 20):
            end = min(start + 19, surah["ayah_count"])
            surah_page.extend([
                f"### {start}–{end}", "",
                " · ".join(f"[[{surah['stem']} {ayah:03d}|{ayah}]]" for ayah in range(start, end + 1)), "",
            ])
        write(f"{surah['stem']}.md", "\n".join(surah_page))

    total_ayahs = sum(surah["ayah_count"] for surah in SURAHS.values())
    home = f"""{frontmatter("Yazılı Tefsir Kütüphanesi", "index", source_count=len(rows), surah_count=len(SURAHS))}# Yazılı Tefsir Kütüphanesi

180 Saniyede Tefsir kanalındaki sûre anlatımlarının, konuşma dilinden yazı diline **çok hafif müdahaleyle** geçirilmiş tam metinleri.

## Sûreler

- [[Ali Imran|Âl-i İmrân — 200 ayet]]
- [[Nisa|Nisâ — 176 ayet]]
- [[Maide|Mâide — 120 ayet]]
- [[Enam|En‘âm — 165 ayet]]
- [[Araf|A‘râf — 206 ayet]]
- [[Inceleme Panosu|İnceleme panosu]]
- [[Metodoloji]]

## Editoryal ilke

Bu wiki bir açıklamanın yeniden açıklaması değildir. Kaynak videonun anlatımı korunur; yalnızca dolgu sözler, yarım başlangıçlar, noktalama ve paragraf yapısı düzenlenir.

- Yazılı kaynak metni: **{len(rows)}**
- Ayet sayfası: **{total_ayahs}**
- Ham transkript: **{len(rows)}**

> [!warning] İnsan kontrolü
> Arapça ibareler, özel isimler ve transkripsiyon belirsizlikleri editoryal kayıt bölümlerinde işaretlenmiştir.
"""
    write("Home.md", home)

    index = [frontmatter("Tefsir Metinleri İndeksi", "index", source_count=len(rows)), "# Tefsir Metinleri İndeksi", ""]
    for key, surah in SURAHS.items():
        index.extend([f"## {surah['name']}", ""])
        for row in sorted(rows_by_surah[key], key=lambda item: (*row_bounds(item), item["file_name"])):
            bounds = row_bounds(row)
            index.append(f"- [[{article_stem(row)}|{surah['name']} {bounds[0]}" + (f"–{bounds[1]}" if bounds[1] != bounds[0] else "") + f" — {Path(row['file_name']).stem}]]")
        index.append("")
    write("Tefsir Metinleri Indeksi.md", "\n".join(index))

    dashboard = [frontmatter("İnceleme Panosu", "dashboard"), "# İnceleme Panosu", ""]
    for key, surah in SURAHS.items():
        dashboard.extend([f"## {surah['name']}", "", "| Ayet | Kullanılan metin | Durum |", "|---:|---:|---|"])
        for ayah in range(1, surah["ayah_count"] + 1):
            count = len(preferred_rows(rows_by_surah[key], ayah))
            dashboard.append(f"| [[{surah['stem']} {ayah:03d}|{ayah}]] | {count} | Hafif editörlü; insan kontrolü bekliyor |")
        dashboard.append("")
    write("Inceleme Panosu.md", "\n".join(dashboard))

    methodology = f"""{frontmatter("Metodoloji", "methodology")}# Metodoloji

## Kaynak katmanları ve kapsam

### Ana ilmî referans

**180 Saniyede Tefsir** kanalı, ayet ayet yayımladığı tefsir sohbetlerinin ana dayanağını Fahreddin er-Râzî'nin *Mefâtîhu'l-Gayb* adlı eseri — yaygın adıyla *Tefsîr-i Kebîr* — olarak tanımlar.

> [!info] Önemli sınır
> Bu wiki *Tefsîr-i Kebîr*'in doğrudan aktarımı, tercümesi veya tenkitli neşri değildir. Buradaki birincil kaynak, kitaptan hareketle hazırlanmış kanal sohbetlerinin fiilen söylenen hâlidir.

### Sohbet ve anlatım katmanı

Metinler, kanalın Türkçe video sohbetlerinin transkriptlerinden hazırlanır. Râzî'ye atfedilen açıklamalar, başka âlimlerden aktarılan görüşler, dil tartışmaları, örnekler ve sunucunun geçiş cümleleri videoda nasıl ayrıştırılıyorsa öyle korunmaya çalışılır. Kitaba bakılarak eksik cümle tamamlama veya videoda bulunmayan görüş ekleme yapılmaz.

### Bu wikiye dâhil edilen kapsam

Bu sürüm, kanaldan seçilmiş **{len(rows)} ayet tefsiri videosunu** ve bunların kapsadığı beş sûre koleksiyonunu içerir:

- **Âl-i İmrân:** 3–200. ayetler. 1–2. ayetleri kapsayan bir kanal videosu tespit edilmediği için bu iki sayfa açıkça kaynaksız olarak işaretlenmiştir.
- **Nisâ:** 1–176. ayetler.
- **Mâide:** 1–120. ayetler.
- **En‘âm:** 1–165. ayetler.
- **A‘râf:** 1–206. ayetler.

Kanalın diğer sûreleri ve bu koleksiyona alınmamış videoları mevcut sürümün kapsamı dışındadır. Toplam **{total_ayahs} ayet sayfası** bulunur; bir video birden fazla ayeti kapsayabilir ve bir ayet için birden fazla dar kapsamlı sohbet gösterilebilir.

### Metnin izlenebilirliği

1. Kanal videosu ve mevcut özgün altyazı/transkript kaynak kaydı oluşturur.
2. **Ham transkript** konuşmanın değiştirilmemiş metnini saklar.
3. **Yazılı tefsir** aynı konuşmayı, anlamına müdahale etmeden yazı diline geçirir.
4. **Ayet sayfası** ilgili ayeti kapsayan en dar aralıklı yazılı sohbetleri bir araya getirir.

Bu nedenle okuyucu, yazılı metinden ham transkripte ve oradan mevcut olduğunda özgün YouTube videosuna geri dönebilir.

## İzin verilen işlemler

- Noktalama ve paragraf düzeni
- Yarım kalmış konuşma başlangıçlarının temizlenmesi
- Anlam taşımayan dolgu sözlerin çıkarılması
- Birebir anlamsal tekrarların azaltılması
- Konu değişimlerinde sınırlı başlıklandırma

## Yasaklanan işlemler

- Özetleme veya yeni sonuç çıkarma
- Haricî bilgi, meal, ayet metni ya da kaynak ekleme
- Râzî'ye, başka bir âlime veya sunucuya ait görüşleri birbirine karıştırma
- Şüpheli terimleri kontrol notu bırakmadan sessizce düzeltme
"""
    write("Metodoloji.md", methodology)

    obsidian = STAGING / ".obsidian"
    obsidian.mkdir()
    (obsidian / "app.json").write_text(json.dumps({"showInlineTitle": True, "newLinkFormat": "shortest"}, indent=2) + "\n")
    (obsidian / "appearance.json").write_text(json.dumps({"baseFontSize": 17, "theme": "obsidian"}, indent=2) + "\n")
    (obsidian / "core-plugins.json").write_text(json.dumps(["file-explorer", "global-search", "backlink", "graph", "outgoing-link", "properties"], indent=2) + "\n")
    (obsidian / "graph.json").write_text(json.dumps({"collapse-filter": True, "showTags": True, "showAttachments": False, "colorGroups": []}, indent=2) + "\n")


def validate() -> dict:
    files = list(STAGING.rglob("*.md"))
    keys = set()
    for path in files:
        relative = path.relative_to(STAGING).with_suffix("").as_posix()
        keys.add(relative.casefold())
        keys.add(path.stem.casefold())
    unresolved = set()
    pattern = re.compile(r"!?\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
    for path in files:
        for target in pattern.findall(path.read_text(encoding="utf-8")):
            if target.strip().casefold() not in keys:
                unresolved.add(target.strip())
    ayah_pages = len(list((STAGING / "Ayetler").rglob("*.md")))
    article_pages = len(list((STAGING / "Tefsir-Metinleri").glob("*.md")))
    raw_pages = len(list((STAGING / "Ham-Transkriptler").glob("*.md")))
    expected_ayahs = sum(surah["ayah_count"] for surah in SURAHS.values())
    if ayah_pages != expected_ayahs or unresolved:
        raise RuntimeError(f"Vault validation failed: ayahs={ayah_pages}, unresolved={sorted(unresolved)}")
    return {"markdown_files": len(files), "ayah_pages": ayah_pages, "article_pages": article_pages, "raw_pages": raw_pages, "unresolved_links": 0}


def activate() -> Path | None:
    archived = None
    if VAULT.exists():
        ARCHIVE.mkdir(exist_ok=True)
        archived = ARCHIVE / f"vault-prose-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        shutil.move(str(VAULT), str(archived))
    shutil.move(str(STAGING), str(VAULT))
    return archived


def main() -> int:
    rows, source_by_row = load_rows()
    results: dict[int, dict] = {}
    cached_count = 0
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(convert, row, source_by_row.get(row["id"])) for row in rows]
        for completed, future in enumerate(as_completed(futures), start=1):
            row_id, result, cached = future.result()
            results[row_id] = result
            cached_count += int(cached)
            if completed % 4 == 0 or completed == len(rows):
                print(f"Converted {completed}/{len(rows)} sources ({cached_count} cached)", flush=True)
    build_vault(rows, source_by_row, results)
    report = validate()
    archived = activate()
    report.update({"active_vault": str(VAULT), "archived_vault": str(archived) if archived else None})
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
