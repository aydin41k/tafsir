#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline import ROOT, call_azure, local_rest, row_range  # noqa: E402

VAULT = ROOT / "vault"
PILOT = VAULT / "Pilot"
CACHE = ROOT / "data/prose-pilot"
PROMPT = (ROOT / "prompts/transcript-to-prose.md").read_text(encoding="utf-8")


def source_stem(row: dict) -> str:
    return f"{row['id']:03d} - {Path(row['file_name']).stem}"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def frontmatter(title: str, kind: str, **extra) -> str:
    data = {
        "title": title,
        "type": kind,
        "review_status": "pilot-review",
        "editorial_level": "light",
        **extra,
    }
    lines = ["---"]
    for key, value in data.items():
        if isinstance(value, (int, float)):
            rendered = str(value)
        else:
            rendered = json.dumps(str(value), ensure_ascii=False)
        lines.append(f"{key}: {rendered}")
    return "\n".join(lines + ["---", ""])


def select_rows() -> tuple[list[dict], dict[int, dict]]:
    rest = local_rest()
    rows = rest.get("media_transcriptions", "select=*&type=eq.youtube&order=id.asc")
    selected = []
    for row in rows:
        bounds = row_range(row)
        if bounds in {(1, 2), (54, 54), (205, 205)}:
            selected.append(row)
    sources = rest.get("media_sources", "select=*&order=id.asc")
    source_by_row = {
        source["media_transcription_id"]: source
        for source in sources if source.get("media_transcription_id")
    }
    if not any(row_range(row) == (1, 2) for row in selected):
        raise RuntimeError("A‘râf 1–2 source was not found")
    if len([row for row in selected if row_range(row) == (54, 54)]) < 5:
        raise RuntimeError("Expected the five A‘râf 54 source videos")
    if not any(row_range(row) == (205, 205) for row in selected):
        raise RuntimeError("A‘râf 205 source was not found")
    return selected, source_by_row


def convert(row: dict, source: dict | None) -> tuple[int, dict]:
    cache = CACHE / f"{row['id']}.json"
    if cache.exists():
        return row["id"], json.loads(cache.read_text(encoding="utf-8"))
    transcript = (row.get("transcription") or "").strip()
    title = (source or {}).get("title") or Path(row["file_name"]).stem
    message = (
        f"SOURCE TITLE: {title}\n"
        f"SOURCE FILE: {row['file_name']}\n"
        f"AYAH RANGE: {row_range(row)}\n\n"
        f"RAW TRANSCRIPT:\n{transcript}"
    )
    result = call_azure(PROMPT, message, max_tokens=12000, model="gpt-5.4")
    article = (result.get("article_markdown") or "").strip()
    ratio = len(article) / max(1, len(transcript))
    if ratio < 0.62:
        result = call_azure(
            PROMPT,
            message + (
                "\n\nIMPORTANT RETRY NOTE: The previous edit was too compressed. "
                "Preserve substantially more of the source detail and wording."
            ),
            max_tokens=14000,
            model="gpt-5.4",
        )
        article = (result.get("article_markdown") or "").strip()
        ratio = len(article) / max(1, len(transcript))
    result["row_id"] = row["id"]
    result["raw_characters"] = len(transcript)
    result["article_characters"] = len(article)
    result["retention_ratio"] = round(ratio, 3)
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return row["id"], result


def raw_page(row: dict, source: dict | None, label: str) -> str:
    title = (source or {}).get("title") or Path(row["file_name"]).stem
    url = (source or {}).get("source_url")
    transcript = (row.get("transcription") or "").strip()
    lines = [
        frontmatter(f"{label} — Ham Transkript", "raw-transcript", row_id=row["id"]),
        f"# {label} — Ham Transkript",
        "",
        f"- Kaynak: [[{source_stem(row)}|{title}]]",
    ]
    if url:
        lines.append(f"- Video: {url}")
    lines.extend(["", "> [!info] Değiştirilmemiş kaynak", "> Aşağıdaki metin yerel `media_transcriptions` kaydından aynen alınmıştır.", "", transcript])
    return "\n".join(lines)


def article_page(row: dict, source: dict | None, result: dict, label: str) -> str:
    title = (result.get("title") or label).strip()
    article = (result.get("article_markdown") or "").strip()
    return "\n".join([
        frontmatter(title, "lightly-edited-prose", row_id=row["id"], retention_ratio=result["retention_ratio"]),
        f"# {title}",
        "",
        "> [!warning] Pilot metin",
        "> Bu metin yalnızca konuşma dilini yazı diline dönüştürmek amacıyla hafifçe düzenlenmiştir. Yeni açıklama veya haricî bilgi eklenmemelidir.",
        "",
        f"Kaynak: [[{source_stem(row)}|{Path(row['file_name']).stem}]] · [[{label} - Ham Transkript]] · [[{label} - Degisiklik Kaydi]]",
        "",
        article,
    ])


def comparison_page(row: dict, result: dict, label: str) -> str:
    transcript = (row.get("transcription") or "").strip()
    article = (result.get("article_markdown") or "").strip()
    changes = [str(item).strip() for item in result.get("editorial_changes") or [] if str(item).strip()]
    uncertainties = [str(item).strip() for item in result.get("uncertainties") or [] if str(item).strip()]
    raw_excerpt = html.escape(transcript[:1800]).replace("\n", "<br>")
    article_excerpt = html.escape(article[:1800]).replace("\n", "<br>")
    lines = [
        frontmatter(f"{label} — Değişiklik Kaydı", "editorial-comparison", row_id=row["id"]),
        f"# {label} — Değişiklik Kaydı",
        "",
        f"- Ham metin: **{result['raw_characters']:,}** karakter",
        f"- Yazılı metin: **{result['article_characters']:,}** karakter",
        f"- Koruma oranı: **%{result['retention_ratio'] * 100:.1f}**",
        f"- [[{label} - Ham Transkript|Tam ham transkript]]",
        f"- [[{label} - Yazili Metin|Tam yazılı metin]]",
        "",
        "## Yan yana örnek",
        "",
        '<div class="comparison-grid">',
        f'<section><h3>Ham transkript</h3><p>{raw_excerpt}</p></section>',
        f'<section><h3>Yazılı metin</h3><p>{article_excerpt}</p></section>',
        "</div>",
        "",
        "## Uygulanan editoryal işlemler",
        "",
    ]
    lines.extend(f"- {item}" for item in changes)
    lines.extend(["", "## İnsan kontrolü gereken noktalar", ""])
    lines.extend([f"- {item}" for item in uncertainties] or ["- Model tarafından özel bir belirsizlik işaretlenmedi."])
    return "\n".join(lines)


def build_pages(rows: list[dict], source_by_row: dict[int, dict], results: dict[int, dict]) -> None:
    PILOT.mkdir(parents=True, exist_ok=True)
    index_lines = [
        frontmatter("Yazılı Tefsir Metni Pilotu", "pilot-index"),
        "# Yazılı Tefsir Metni Pilotu",
        "",
        "Bu pilot, video açıklamasını yeniden açıklamak yerine transkripti doğrudan, aslına sadık yazılı metne dönüştürür.",
        "",
        "## Editoryal sözleşme",
        "",
        "- Yeni bilgi, yorum veya sonuç eklenmez.",
        "- Konuşmacının argüman sırası ve atıfları korunur.",
        "- Yalnızca dolgu, yarım başlangıçlar, noktalama ve paragraf yapısı düzenlenir.",
        "- Şüpheli terimler sessizce düzeltilmez; insan kontrolüne işaretlenir.",
        "",
        "## İncelenecek örnekler",
        "",
    ]

    groups: dict[tuple[int, int], list[dict]] = {}
    for row in rows:
        groups.setdefault(row_range(row), []).append(row)

    for bounds in [(1, 2), (54, 54), (205, 205)]:
        group = groups[bounds]
        group.sort(key=lambda row: (
            (source_by_row.get(row["id"]) or {}).get("published_at") or "9999",
            row["file_name"],
        ))
        group_label = f"Araf {bounds[0]}" if bounds[0] == bounds[1] else f"Araf {bounds[0]}-{bounds[1]}"
        if bounds == (54, 54):
            combined_sections = []
            combined_changes = []
            combined_uncertainties = []
            raw_chars = article_chars = 0
            for position, row in enumerate(group, start=1):
                source = source_by_row.get(row["id"])
                result = results[row["id"]]
                label = f"Araf 54 - Kaynak {position}"
                write(PILOT / f"{label} - Ham Transkript.md", raw_page(row, source, label))
                section_title = result.get("title") or ((source or {}).get("title") or label)
                combined_sections.extend([f"## {section_title}", "", result.get("article_markdown") or "", ""])
                combined_changes.extend(result.get("editorial_changes") or [])
                combined_uncertainties.extend(result.get("uncertainties") or [])
                raw_chars += result["raw_characters"]
                article_chars += result["article_characters"]
            combined = {
                "title": "A‘râf 54 — Yazılı Tefsir Metni",
                "article_markdown": "\n".join(combined_sections).strip(),
                "editorial_changes": list(dict.fromkeys(combined_changes)),
                "uncertainties": list(dict.fromkeys(combined_uncertainties)),
                "raw_characters": raw_chars,
                "article_characters": article_chars,
                "retention_ratio": round(article_chars / max(1, raw_chars), 3),
            }
            synthetic_row = {**group[0], "id": group[0]["id"], "transcription": "\n\n".join((row.get("transcription") or "") for row in group)}
            article_label = "Araf 54"
            write(PILOT / "Araf 54 - Ham Transkript.md", raw_page(synthetic_row, source_by_row.get(group[0]["id"]), article_label))
            write(PILOT / "Araf 54 - Yazili Metin.md", article_page(synthetic_row, source_by_row.get(group[0]["id"]), combined, article_label))
            write(PILOT / "Araf 54 - Degisiklik Kaydi.md", comparison_page(synthetic_row, combined, article_label))
            index_lines.extend(["### A‘râf 54", "", "- [[Araf 54 - Yazili Metin|Birleştirilmiş yazılı metin]]", "- [[Araf 54 - Degisiklik Kaydi|Değişiklik kaydı ve karşılaştırma]]", ""])
        else:
            row = group[0]
            source = source_by_row.get(row["id"])
            result = results[row["id"]]
            label = group_label
            write(PILOT / f"{label} - Ham Transkript.md", raw_page(row, source, label))
            write(PILOT / f"{label} - Yazili Metin.md", article_page(row, source, result, label))
            write(PILOT / f"{label} - Degisiklik Kaydi.md", comparison_page(row, result, label))
            index_lines.extend([
                f"### A‘râf {bounds[0]}" + (f"–{bounds[1]}" if bounds[1] != bounds[0] else ""),
                "",
                f"- [[{label} - Yazili Metin|Yazılı metin]]",
                f"- [[{label} - Ham Transkript|Ham transkript]]",
                f"- [[{label} - Degisiklik Kaydi|Değişiklik kaydı ve karşılaştırma]]",
                "",
            ])

    write(PILOT / "Pilot - Baslangic.md", "\n".join(index_lines))
    home = VAULT / "Home.md"
    if home.exists():
        content = home.read_text(encoding="utf-8")
        link = "- [[Pilot - Baslangic|Yazılı tefsir metni pilotu]]"
        if link not in content:
            content = content.replace("## Başlangıç\n", "## Başlangıç\n\n" + link + "\n", 1)
            home.write_text(content, encoding="utf-8")


def main() -> int:
    rows, source_by_row = select_rows()
    results: dict[int, dict] = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(convert, row, source_by_row.get(row["id"])) for row in rows]
        for completed, future in enumerate(as_completed(futures), start=1):
            row_id, result = future.result()
            results[row_id] = result
            print(
                f"[{completed}/{len(rows)}] row {row_id}: retention {result['retention_ratio']:.1%}",
                flush=True,
            )
    build_pages(rows, source_by_row, results)
    print(json.dumps({"pilot_sources": len(rows), "pilot_path": str(PILOT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
