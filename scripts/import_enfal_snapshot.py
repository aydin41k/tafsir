#!/usr/bin/env python3
"""Add the prepared YouTube Enfal transcripts without mutating existing rows."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from editorial_style import normalize_sentence_initial_ayah_ordinals

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"
FIRST_LOCAL_ID = 372
VERIFIED_URLS = {
    161: "https://www.youtube.com/watch?v=hC9aWGqbGtI",
    163: "https://www.youtube.com/watch?v=HYwLTk4H9ts",
}


def bounds(file_name: str) -> tuple[int, int]:
    stem = Path(file_name).stem
    if "sebebi nuzul" in stem.casefold():
        return 1, 1
    match = re.search(r"\bEnfal\s+(\d+)(?:-(\d+))?", stem, re.IGNORECASE)
    if not match:
        raise ValueError(f"Cannot determine ayah range: {file_name}")
    start, end = int(match.group(1)), int(match.group(2) or match.group(1))
    # Enfal 67-1 and Enfal 67-2 are two parts of ayah 67, not reversed ranges.
    if start == 67 and end in {1, 2}:
        end = 67
    if not 1 <= start <= end <= 75:
        raise ValueError(f"Invalid ayah range: {file_name}")
    return start, end


def frontmatter(title: str, kind: str, **values: object) -> str:
    data = {"title": title, "type": kind, "review_status": "machine-edited", **values}
    lines = ["---"]
    for key, value in data.items():
        rendered = str(value).lower() if isinstance(value, bool) else str(value) if isinstance(value, (int, float)) else json.dumps(str(value), ensure_ascii=False)
        lines.append(f"{key}: {rendered}")
    return "\n".join(lines + ["---", ""])


def paragraphize(transcript: str) -> str:
    text = normalize_sentence_initial_ayah_ordinals(re.sub(r"\s+", " ", transcript).strip())
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return "\n\n".join(" ".join(sentences[index:index + 5]) for index in range(0, len(sentences), 5))


def article_stem(row: dict) -> str:
    return f"{row['local_id']:03d} - {Path(row['file_name']).stem}"


def raw_stem(row: dict) -> str:
    return f"Ham - {article_stem(row)}"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def build(snapshot: Path) -> None:
    prepared = json.loads(snapshot.read_text(encoding="utf-8"))
    selected = [row for row in prepared if row.get("type") == "youtube"]
    if len(selected) != 62:
        raise RuntimeError(f"Expected 62 YouTube records, found {len(selected)}")

    rows = []
    for local_id, source in enumerate(selected, FIRST_LOCAL_ID):
        if not str(source.get("transcription") or "").strip() or not str(source.get("description") or "").strip():
            raise RuntimeError(f"Incomplete prepared row {source.get('id')}")
        start, end = bounds(source["file_name"])
        rows.append({**source, "remote_id": source["id"], "local_id": local_id, "ayah_start": start, "ayah_end": end, "source_url": VERIFIED_URLS.get(source["id"])})

    coverage = {ayah for row in rows for ayah in range(row["ayah_start"], row["ayah_end"] + 1)}
    if coverage != set(range(1, 76)):
        raise RuntimeError(f"Incomplete Enfal coverage: {sorted(set(range(1, 76)) - coverage)}")

    inventory = []
    for row in rows:
        title = Path(row["file_name"]).stem
        article = [
            frontmatter(title, "tefsir-text", editorial_level="light", row_id=row["local_id"], surah_key="enfal", surah="Enfâl", surah_number=8, ayah_start=row["ayah_start"], ayah_end=row["ayah_end"], retention_ratio=1.0),
            f"# {title}", "", "> [!info] Editoryal seviye: hafif", "> Bu metin kaynak kaydın transkriptidir. Yalnızca konuşma akışını okunabilir paragraflara ayıran mekanik düzenleme uygulanmıştır; yeni açıklama, özet veya haricî bilgi eklenmemiştir.", "", "## Kaynak bilgisi", "", f"- Kayıt: `{row['file_name']}`", f"- Ayet aralığı: Enfâl {row['ayah_start']}" + (f"–{row['ayah_end']}" if row["ayah_end"] != row["ayah_start"] else ""), f"- Ham transkript: [[{raw_stem(row)}]]",
        ]
        if row["source_url"]:
            article.append(f"- Video: {row['source_url']}")
        article.extend(["", "---", "", paragraphize(row["transcription"]), "", "---", "", "<details>", "<summary>Editoryal kayıt ve insan kontrolü</summary>", "", "### Uygulanan işlemler", "", "- Kaynak transkript anlamı değiştirilmeden paragraflara ayrıldı.", "", "### Kontrol gereken noktalar", "", "- Arapça ibareler, özel isimler ve otomatik transkripsiyon belirsizlikleri insan kontrolü bekliyor.", "", "</details>"])
        write(VAULT / "Tefsir-Metinleri" / f"{article_stem(row)}.md", "\n".join(article))

        raw = [frontmatter(f"Ham Transkript — {title}", "raw-transcript", row_id=row["local_id"], surah_key="enfal", surah="Enfâl", surah_number=8, ayah_start=row["ayah_start"], ayah_end=row["ayah_end"]), f"# Ham Transkript — {title}", "", "> [!warning] Değiştirilmemiş kaynak", "> Bu sayfa hazırlanmış kaynak kaydındaki metni aynen korur.", "", f"Yazılı sürüm: [[{article_stem(row)}]]"]
        if row["source_url"]:
            raw.append(f"Video: {row['source_url']}")
        raw.extend(["", "---", "", row["transcription"]])
        write(VAULT / "Ham-Transkriptler" / f"{raw_stem(row)}.md", "\n".join(raw))
        inventory.append({key: row[key] for key in ("local_id", "remote_id", "file_name", "ayah_start", "ayah_end", "source_url")})

    for ayah in range(1, 76):
        covering = [row for row in rows if row["ayah_start"] <= ayah <= row["ayah_end"]]
        minimum = min(row["ayah_end"] - row["ayah_start"] for row in covering)
        chosen = [row for row in covering if row["ayah_end"] - row["ayah_start"] == minimum]
        lines = [frontmatter(f"Enfâl {ayah}", "ayah", surah_key="enfal", surah="Enfâl", surah_number=8, ayah=ayah, source_count=len(chosen)), f"# Enfâl {ayah}", "", "> [!info] Kaynak metin", "> Aşağıdaki içerik, bu ayeti kapsayan en dar aralıklı video transkriptlerinden yazı diline geçirilmiştir."]
        for row in chosen:
            label = f"Enfâl {row['ayah_start']}" + (f"–{row['ayah_end']}" if row["ayah_end"] != row["ayah_start"] else "")
            lines.extend(["", f"## {label}", "", f"![[{article_stem(row)}]]"])
        previous = f"[[Enfal {ayah - 1:03d}|← {ayah - 1}]]" if ayah > 1 else ""
        following = f"[[Enfal {ayah + 1:03d}|{ayah + 1} →]]" if ayah < 75 else ""
        lines.extend(["", "---", "", f"{previous}  {following}".strip()])
        write(VAULT / "Ayetler" / "Enfal" / f"Enfal {ayah:03d}.md", "\n".join(lines))

    surah = [frontmatter("Enfâl", "surah", surah_key="enfal", surah_number=8, ayah_count=75, source_count=len(rows)), "# Enfâl", "", "## Ayet haritası", ""]
    for start in range(1, 76, 20):
        end = min(start + 19, 75)
        surah.extend([f"### {start}–{end}", "", " · ".join(f"[[Enfal {ayah:03d}|{ayah}]]" for ayah in range(start, end + 1)), ""])
    write(VAULT / "Enfal.md", "\n".join(surah))
    write(ROOT / "data" / "channel-enfal.json", json.dumps(inventory, ensure_ascii=False, indent=2))

    index_path = VAULT / "Tefsir Metinleri Indeksi.md"
    index = index_path.read_text(encoding="utf-8").rstrip()
    if "\n## Enfâl\n" not in index:
        index += "\n\n## Enfâl\n\n" + "\n".join(
            f"- [[{article_stem(row)}|Enfâl {row['ayah_start']}" +
            (f"–{row['ayah_end']}" if row["ayah_end"] != row["ayah_start"] else "") +
            f" — {Path(row['file_name']).stem}]]"
            for row in sorted(rows, key=lambda item: (item["ayah_start"], item["ayah_end"], item["file_name"]))
        )
        write(index_path, index)

    dashboard_path = VAULT / "Inceleme Panosu.md"
    dashboard = dashboard_path.read_text(encoding="utf-8").rstrip()
    if "\n## Enfâl\n" not in dashboard:
        dashboard += "\n\n## Enfâl\n\n| Ayet | Kullanılan metin | Durum |\n|---:|---:|---|\n"
        for ayah in range(1, 76):
            covering = [row for row in rows if row["ayah_start"] <= ayah <= row["ayah_end"]]
            minimum = min(row["ayah_end"] - row["ayah_start"] for row in covering)
            count = sum(row["ayah_end"] - row["ayah_start"] == minimum for row in covering)
            dashboard += f"| [[Enfal {ayah:03d}|{ayah}]] | {count} | Hafif editörlü; insan kontrolü bekliyor |\n"
        write(dashboard_path, dashboard)

    print(json.dumps({"imported": len(rows), "local_ids": [rows[0]["local_id"], rows[-1]["local_id"]], "coverage": len(coverage), "verified_urls": sum(bool(row["source_url"]) for row in rows)}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    build(parser.parse_args().snapshot)
