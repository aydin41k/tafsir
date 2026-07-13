#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
import sys
import unicodedata
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline import ROOT, call_azure, local_rest, row_range  # noqa: E402

VAULT = ROOT / "vault"
CACHE = ROOT / "data/analysis"


def safe_text(value) -> str:
    return str(value or "").strip()


def note_slug(value: str) -> str:
    folded = "".join(
        char for char in unicodedata.normalize("NFKD", value.replace("ı", "i"))
        if not unicodedata.combining(char)
    )
    folded = re.sub(r"[^A-Za-z0-9ÇĞİÖŞÜçğıöşü]+", "-", folded).strip("-")
    return folded or "not"


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def write_note(relative: str, body: str) -> None:
    path = VAULT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip() + "\n", encoding="utf-8")


def source_stem(row: dict) -> str:
    return f"{row['id']:03d} - {Path(row['file_name']).stem}"


def source_payload(row: dict, source: dict | None) -> dict:
    transcription = safe_text(row.get("transcription"))
    description = safe_text(row.get("description"))
    return {
        "row_id": row["id"],
        "file_name": row["file_name"],
        "title": (source or {}).get("title") or Path(row["file_name"]).stem,
        "ayah_range": list(row_range(row) or []),
        "description": description[:3500],
        "transcript_excerpt": transcription[:1500],
    }


def analyse_rows(rows: list[dict], source_by_row: dict[int, dict]) -> dict[int, dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    prompt = (ROOT / "prompts/wiki-analysis.md").read_text(encoding="utf-8")
    analyses: dict[int, dict] = {}
    pending: list[dict] = []
    for row in rows:
        path = CACHE / f"{row['id']}.json"
        if path.exists():
            analyses[row["id"]] = json.loads(path.read_text(encoding="utf-8"))
        else:
            pending.append(row)

    def analyse_one(row: dict) -> tuple[int, dict]:
        response = call_azure(
            prompt,
            "Return {\"analyses\": [one item]}.\n\nSOURCE:\n" +
            json.dumps(source_payload(row, source_by_row.get(row["id"])), ensure_ascii=False),
            max_tokens=1800,
            model="gpt-5.4",
        )
        return row["id"], (response.get("analyses") or [response])[0]

    if pending:
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(analyse_one, row) for row in pending]
            for completed, future in enumerate(as_completed(futures), start=1):
                row_id, analysis = future.result()
                analysis["row_id"] = row_id
                (CACHE / f"{row_id}.json").write_text(
                    json.dumps(analysis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
                )
                analyses[row_id] = analysis
                if completed % 4 == 0 or completed == len(pending):
                    print(f"Analysed {completed}/{len(pending)} uncached sources", flush=True)
    return analyses


def frontmatter(title: str, kind: str, extra: dict | None = None) -> str:
    values = {
        "title": title,
        "type": kind,
        "review_status": "machine-generated",
        **(extra or {}),
    }
    lines = ["---"]
    for key, value in values.items():
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif isinstance(value, (int, float)):
            rendered = str(value)
        else:
            rendered = yaml_string(str(value))
        lines.append(f"{key}: {rendered}")
    return "\n".join(lines + ["---", ""])


def build_vault(rows: list[dict], sources: list[dict], analyses: dict[int, dict]) -> None:
    if VAULT.exists():
        shutil.rmtree(VAULT)
    (VAULT / ".obsidian").mkdir(parents=True)
    source_by_row = {source["media_transcription_id"]: source for source in sources if source.get("media_transcription_id")}
    rows_by_ayah: dict[int, list[dict]] = defaultdict(list)
    concepts: dict[str, dict] = {}
    figures: dict[str, dict] = {}

    for row in rows:
        bounds = row_range(row)
        if not bounds:
            continue
        for ayah in range(bounds[0], bounds[1] + 1):
            rows_by_ayah[ayah].append(row)
        analysis = analyses[row["id"]]
        for item in analysis.get("concepts") or []:
            name = safe_text(item.get("name"))
            if name:
                key = name.casefold()
                concepts.setdefault(key, {"name": name, "mentions": []})["mentions"].append((row, safe_text(item.get("note"))))
        for item in analysis.get("figures") or []:
            name = safe_text(item.get("name"))
            if name:
                key = name.casefold()
                figures.setdefault(key, {"name": name, "mentions": []})["mentions"].append((row, safe_text(item.get("note"))))

    concept_stems = {key: note_slug(item["name"]) for key, item in concepts.items()}
    figure_stems = {key: note_slug(item["name"]) for key, item in figures.items()}

    for row in rows:
        source = source_by_row.get(row["id"])
        analysis = analyses[row["id"]]
        bounds = row_range(row) or (0, 0)
        title = (source or {}).get("title") or Path(row["file_name"]).stem
        source_link = (source or {}).get("source_url")
        lines = [
            frontmatter(title, "source", {
                "row_id": row["id"],
                "ayah_start": bounds[0],
                "ayah_end": bounds[1],
                "transcript_status": "available" if safe_text(row.get("transcription")) else "missing",
            }),
            f"# {title}",
            "",
            "> [!warning] İnceleme durumu",
            "> Bu sayfadaki özet ve kavram etiketleri makine tarafından üretilmiştir. Yorumlar video kaynağına atfedilmelidir.",
            "",
            "## Kaynak",
            "",
            f"- Dosya: `{row['file_name']}`",
            f"- Ayet aralığı: [[Araf {bounds[0]:03d}|A‘râf {bounds[0]}]]" + (f"–[[Araf {bounds[1]:03d}|{bounds[1]}]]" if bounds[1] != bounds[0] else ""),
        ]
        if source_link:
            lines.append(f"- YouTube: {source_link}")
        lines.extend(["", "## Kaynak özeti", "", safe_text(analysis.get("summary")) or "Özet üretilemedi."])
        points = [safe_text(point) for point in analysis.get("key_points") or [] if safe_text(point)]
        if points:
            lines.extend(["", "## Temel noktalar", ""] + [f"- {point}" for point in points])
        concept_links = []
        for item in analysis.get("concepts") or []:
            name = safe_text(item.get("name"))
            if name and name.casefold() in concept_stems:
                concept_links.append(f"[[{concept_stems[name.casefold()]}|{name}]]")
        if concept_links:
            lines.extend(["", "## Kavramlar", "", " · ".join(concept_links)])
        figure_links = []
        for item in analysis.get("figures") or []:
            name = safe_text(item.get("name"))
            if name and name.casefold() in figure_stems:
                figure_links.append(f"[[{figure_stems[name.casefold()]}|{name}]]")
        if figure_links:
            lines.extend(["", "## Kişiler ve topluluklar", "", " · ".join(figure_links)])
        questions = [safe_text(item) for item in analysis.get("questions") or [] if safe_text(item)]
        if questions:
            lines.extend(["", "## Ele alınan sorular", ""] + [f"- {item}" for item in questions])
        cautions = [safe_text(item) for item in analysis.get("cautions") or [] if safe_text(item)]
        if cautions:
            lines.extend(["", "## Belirsizlikler ve kontrol notları", ""] + [f"- {item}" for item in cautions])
        description = safe_text(row.get("description"))
        if description:
            lines.extend(["", "## Kayıtlı video açıklaması", "", description])
        transcript = safe_text(row.get("transcription"))
        if transcript:
            lines.extend(["", "## Transkript", "", "<details>", "<summary>Tam transkripti göster</summary>", "", transcript, "", "</details>"])
        write_note(f"Kaynaklar/{source_stem(row)}.md", "\n".join(lines))

    for ayah in range(1, 207):
        linked_rows = rows_by_ayah.get(ayah, [])
        lines = [
            frontmatter(f"A‘râf {ayah}", "ayah", {"surah": "A‘râf", "ayah": ayah, "source_count": len(linked_rows)}),
            f"# A‘râf {ayah}",
            "",
            "> [!info] Kapsam",
            "> Bu sayfa ayetin Arapça metnini veya mealini üretmez. Yalnızca kanalın bu ayeti kapsayan videolarından kaynak bağlantılı notları toplar.",
        ]
        if not linked_rows:
            lines.extend(["", "> [!danger] Kaynak eksik", "> Bu ayeti kapsayan bir transkript bulunamadı."])
        for row in linked_rows:
            analysis = analyses[row["id"]]
            lines.extend([
                "", f"## [[{source_stem(row)}|{Path(row['file_name']).stem}]]", "",
                safe_text(analysis.get("summary")) or "Özet üretilemedi.", "",
            ])
            for point in analysis.get("key_points") or []:
                if safe_text(point):
                    lines.append(f"- {safe_text(point)}")
        previous_link = f"[[Araf {ayah - 1:03d}|← {ayah - 1}]]" if ayah > 1 else ""
        next_link = f"[[Araf {ayah + 1:03d}|{ayah + 1} →]]" if ayah < 206 else ""
        lines.extend(["", "---", "", f"{previous_link}  {next_link}".strip()])
        write_note(f"Ayetler/Araf {ayah:03d}.md", "\n".join(lines))

    for key, item in sorted(concepts.items(), key=lambda pair: pair[1]["name"].casefold()):
        name = item["name"]
        lines = [frontmatter(name, "concept", {"source_count": len(item["mentions"])}), f"# {name}", ""]
        for row, note in item["mentions"]:
            lines.extend([f"## [[{source_stem(row)}|{Path(row['file_name']).stem}]]", "", note or "Bu kavram kaynakta anılıyor.", ""])
        write_note(f"Kavramlar/{concept_stems[key]}.md", "\n".join(lines))

    for key, item in sorted(figures.items(), key=lambda pair: pair[1]["name"].casefold()):
        name = item["name"]
        lines = [frontmatter(name, "figure", {"source_count": len(item["mentions"])}), f"# {name}", ""]
        for row, note in item["mentions"]:
            lines.extend([f"## [[{source_stem(row)}|{Path(row['file_name']).stem}]]", "", note or "Bu kaynakta anılıyor.", ""])
        write_note(f"Kisiler-ve-Topluluklar/{figure_stems[key]}.md", "\n".join(lines))

    source_count = len(rows)
    missing = [ayah for ayah in range(1, 207) if not rows_by_ayah.get(ayah)]
    home = f"""{frontmatter("A‘râf Tefsir Wiki", "index", {"source_count": source_count})}# A‘râf Tefsir Wiki

180 Saniyede Tefsir kanalındaki A‘râf videolarından oluşturulan, kaynak izlenebilir Obsidian kasası.

## Başlangıç

- [[Araf|Sûre haritası]]
- [[Inceleme Panosu|İnceleme panosu]]
- [[Metodoloji]]
- [[Kavram Indeksi|Kavram indeksi]]
- [[Kaynak Indeksi|Kaynak indeksi]]

## Durum

- YouTube kaynak kaydı: **{source_count}**
- Ayet sayfası: **206**
- Kaynaksız ayet: **{len(missing)}**

> [!warning] Editöryal durum
> Sentez sayfaları makine tarafından üretilmiştir. Her iddia kaynak transkriptiyle karşılaştırılmalıdır.
"""
    write_note("Home.md", home)

    section_lines = [frontmatter("A‘râf", "surah", {"ayah_count": 206}), "# A‘râf", "", "## Ayet haritası", ""]
    for start in range(1, 207, 20):
        end = min(start + 19, 206)
        section_lines.extend([f"### {start}–{end}", "", " · ".join(f"[[Araf {ayah:03d}|{ayah}]]" for ayah in range(start, end + 1)), ""])
    write_note("Araf.md", "\n".join(section_lines))

    dashboard = [frontmatter("İnceleme Panosu", "dashboard"), "# İnceleme Panosu", "", "İnsan incelemesi için önerilen sıra: kaynak özeti → ayet sayfası → kavram sayfası.", "", "| Ayet | Kaynak | Durum |", "|---:|---:|---|"]
    for ayah in range(1, 207):
        count = len(rows_by_ayah.get(ayah, []))
        status = "Kaynak var; inceleme bekliyor" if count else "Kaynak eksik"
        dashboard.append(f"| [[Araf {ayah:03d}|{ayah}]] | {count} | {status} |")
    write_note("Inceleme Panosu.md", "\n".join(dashboard))

    concept_index = [frontmatter("Kavram İndeksi", "index"), "# Kavram İndeksi", ""]
    concept_index.extend(f"- [[{concept_stems[key]}|{item['name']}]] ({len(item['mentions'])})" for key, item in sorted(concepts.items(), key=lambda pair: pair[1]["name"].casefold()))
    write_note("Kavram Indeksi.md", "\n".join(concept_index))

    source_index = [frontmatter("Kaynak İndeksi", "index"), "# Kaynak İndeksi", ""]
    source_index.extend(f"- [[{source_stem(row)}|{Path(row['file_name']).stem}]]" for row in rows)
    write_note("Kaynak Indeksi.md", "\n".join(source_index))

    methodology = f"""{frontmatter("Metodoloji", "methodology")}# Metodoloji

## Katmanlar

1. `media_transcriptions` kaynak transkript ve açıklamalarını saklar.
2. `media_sources` video kimliği, URL ve ayet aralığını saklar.
3. `data/analysis` yeniden üretilebilir makine analizlerini saklar.
4. Bu Obsidian kasası analizleri kaynak bağlantılı notlara dönüştürür.

## Güvenlik kuralları

- Kur’an metni veya meal model hafızasından üretilmez.
- Râzî’ye veya başka bir müfessire atfedilen görüşler kaynak videoya atıfla sunulur.
- Makine özeti, transkriptin yerine geçmez.
- Transkripsiyon hatası ihtimali taşıyan özel isim ve Arapça terimler insan tarafından kontrol edilir.
- `review_status: machine-generated` etiketi insan incelemesi tamamlanana kadar korunur.
"""
    write_note("Metodoloji.md", methodology)

    obsidian = VAULT / ".obsidian"
    (obsidian / "app.json").write_text(json.dumps({"showInlineTitle": True, "newLinkFormat": "shortest"}, indent=2) + "\n")
    (obsidian / "appearance.json").write_text(json.dumps({"baseFontSize": 17, "theme": "obsidian"}, indent=2) + "\n")
    (obsidian / "core-plugins.json").write_text(json.dumps(["file-explorer", "global-search", "backlink", "graph", "outgoing-link", "tag-pane", "properties"], indent=2) + "\n")
    (obsidian / "graph.json").write_text(json.dumps({"collapse-filter": True, "showTags": True, "showAttachments": False, "colorGroups": []}, indent=2) + "\n")


def main() -> int:
    rest = local_rest()
    all_rows = rest.get("media_transcriptions", "select=*&type=eq.youtube&order=id.asc")
    rows = [row for row in all_rows if row_range(row)]
    sources = rest.get("media_sources", "select=*&order=ayah_start.asc")
    source_by_row = {source["media_transcription_id"]: source for source in sources if source.get("media_transcription_id")}
    analyses = analyse_rows(rows, source_by_row)
    build_vault(rows, sources, analyses)
    print(json.dumps({
        "source_pages": len(rows),
        "ayah_pages": 206,
        "vault": str(VAULT),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
