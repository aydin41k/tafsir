#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import unicodedata
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline import (  # noqa: E402
    AUDIO,
    CHANNEL_URL,
    DATA,
    ROOT,
    TRANSCRIBE_PY,
    call_azure,
    fetch_full_metadata,
    local_rest,
    render_description,
    transcript_from_json3,
    upsert_source,
)

SURAHS = {
    "ali-imran": {
        "key": "ali-imran",
        "name": "Âl-i İmrân",
        "source_tokens": ["al-i imran"],
        "file_stem": "Ali Imran",
        "number": 3,
        "ayah_count": 200,
        "allowed_missing_ayahs": [1, 2],
        "range_overrides": {},
    },
    "nisa": {
        "key": "nisa",
        "name": "Nisâ",
        "source_tokens": ["nisa"],
        "file_stem": "Nisa",
        "number": 4,
        "ayah_count": 176,
        "allowed_missing_ayahs": [],
        "range_overrides": {"P8Geq0DImKE": [163, 170]},
    },
    "maide": {
        "key": "maide",
        "name": "Mâide",
        "source_tokens": ["maide"],
        "file_stem": "Maide",
        "number": 5,
        "ayah_count": 120,
        "allowed_missing_ayahs": [],
        "range_overrides": {},
    },
    "enam": {
        "key": "enam",
        "name": "En‘âm",
        "source_tokens": ["enam"],
        "file_stem": "Enam",
        "number": 6,
        "ayah_count": 165,
        "allowed_missing_ayahs": [],
        "range_overrides": {},
    },
}


def fold(value: str) -> str:
    value = value.replace("ı", "i").replace("İ", "I")
    return "".join(
        char for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    ).lower()


def parse_range(title: str, tokens: list[str], ayah_count: int) -> tuple[int, int] | None:
    normalized = fold(title)
    positions = [normalized.find(token) for token in tokens if token in normalized]
    if not positions:
        return None
    tail = normalized[min(positions):]
    numbers = [int(value) for value in re.findall(r"(?<!\d)(\d{1,3})(?!\d)", tail)]
    numbers = [value for value in numbers if 1 <= value <= ayah_count]
    if not numbers:
        return None
    start, end = numbers[0], numbers[-1]
    if end < start:
        end = start
    if not (1 <= start <= end <= ayah_count):
        return None
    return start, end


def discover(config: dict) -> list[dict]:
    cache = DATA / "channel-all.json"
    if cache.exists():
        channel = json.loads(cache.read_text(encoding="utf-8"))
    else:
        raw = subprocess.check_output(
            ["yt-dlp", "--js-runtimes", "node", "--flat-playlist", "--dump-single-json", CHANNEL_URL],
            text=True,
        )
        channel = json.loads(raw)
        cache.write_text(json.dumps(channel, ensure_ascii=False) + "\n", encoding="utf-8")
    videos = []
    for item in channel.get("entries") or []:
        title = item.get("title") or ""
        if not any(token in fold(title) for token in config["source_tokens"]):
            continue
        override = config.get("range_overrides", {}).get(item["id"])
        bounds = tuple(override) if override else parse_range(title, config["source_tokens"], config["ayah_count"])
        if not bounds:
            continue
        videos.append({
            "id": item["id"],
            "title": title,
            "url": item.get("url") or f"https://www.youtube.com/watch?v={item['id']}",
            "duration": item.get("duration"),
            "ayah_start": bounds[0],
            "ayah_end": bounds[1],
            "surah_key": config["key"],
            "surah_name": config["name"],
            "surah_number": config["number"],
        })
    videos.sort(key=lambda item: (item["ayah_start"], item["ayah_end"], item["title"]))
    path = DATA / f"channel-{config['key']}.json"
    path.write_text(json.dumps(videos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return videos


def validate_inventory(videos: list[dict], config: dict) -> None:
    coverage = set()
    for video in videos:
        coverage.update(range(video["ayah_start"], video["ayah_end"] + 1))
    missing = sorted(set(range(1, config["ayah_count"] + 1)) - coverage)
    unexpected_missing = sorted(set(missing) - set(config.get("allowed_missing_ayahs", [])))
    if unexpected_missing:
        raise RuntimeError(f"Incomplete {config['name']} inventory; unexpected missing ayahs: {unexpected_missing}")
    print(json.dumps({
        "surah": config["name"],
        "videos": len(videos),
        "covered_ayahs": len(coverage),
        "missing_ayahs": missing,
        "allowed_channel_gaps": config.get("allowed_missing_ayahs", []),
    }, ensure_ascii=False))


def canonical_names(videos: list[dict], config: dict) -> dict[str, str]:
    counts = Counter((video["ayah_start"], video["ayah_end"]) for video in videos)
    names = {}
    for video in videos:
        start, end = video["ayah_start"], video["ayah_end"]
        label = str(start) if start == end else f"{start}-{end}"
        suffix = f" - {video['id']}" if counts[(start, end)] > 1 else ""
        names[video["id"]] = f"{config['file_stem']} {label}{suffix}.mp3"
    return names


def source_one(video: dict, config: dict) -> tuple[str, str]:
    target = AUDIO / config["key"] / video["id"]
    target.mkdir(parents=True, exist_ok=True)
    info_path = target / "source.info.json"
    transcript = target / "transcript.txt"
    if transcript.exists() and info_path.exists():
        return video["id"], "caption"
    if yt_dlp is None:
        fetch_full_metadata(video, target, download=True)
    else:
        options = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["tr-orig"],
            "subtitlesformat": "json3",
            "writeinfojson": True,
            "outtmpl": str(target / "source.%(ext)s"),
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.extract_info(video["url"], download=True)
        caption = target / "source.tr-orig.json3"
        if caption.exists():
            transcript.write_text(transcript_from_json3(caption) + "\n", encoding="utf-8")
            (target / "transcript.origin.txt").write_text("youtube_auto_captions\n", encoding="utf-8")
        if not transcript.exists():
            audio_options = {
                "quiet": True,
                "no_warnings": True,
                "format": "bestaudio/best",
                "outtmpl": str(target / "source.%(ext)s"),
                "writeinfojson": True,
                "noplaylist": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "0",
                }],
            }
            with yt_dlp.YoutubeDL(audio_options) as ydl:
                ydl.extract_info(video["url"], download=True)
    if transcript.exists():
        return video["id"], "caption"
    audio = target / "source.mp3"
    if not audio.exists():
        raise RuntimeError(f"No caption or audio for {video['id']}")
    return video["id"], "audio"


def source_all(videos: list[dict], config: dict) -> None:
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(source_one, video, config): video for video in videos}
        for index, future in enumerate(as_completed(futures), start=1):
            video_id, mode = future.result()
            print(f"[{index}/{len(videos)}] sourced {video_id} ({mode})", flush=True)

    jobs = []
    for video in videos:
        target = AUDIO / config["key"] / video["id"]
        transcript = target / "transcript.txt"
        audio = target / "source.mp3"
        if not transcript.exists() and audio.exists():
            jobs.append({"audio": str(audio), "transcript": str(transcript)})
    if jobs:
        manifest = DATA / f"transcribe-{config['key']}.json"
        manifest.write_text(json.dumps(jobs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        subprocess.check_call([str(TRANSCRIBE_PY), str(ROOT / "scripts/transcribe_helper.py"), "--batch", str(manifest)])
        for job in jobs:
            Path(job["transcript"]).with_name("transcript.origin.txt").write_text(
                "local_faster_whisper\n", encoding="utf-8"
            )
    print(json.dumps({"sourced": len(videos), "local_transcriptions": len(jobs)}, ensure_ascii=False))


def description_for(video: dict, config: dict, prompt: str) -> tuple[str, dict]:
    target = AUDIO / config["key"] / video["id"]
    generated_path = target / "description.generated.json"
    if generated_path.exists():
        return video["id"], json.loads(generated_path.read_text(encoding="utf-8"))
    transcript = (target / "transcript.txt").read_text(encoding="utf-8").strip()
    message = (
        f"Source video: {video['title']}\n"
        f"{config['name']} {video['ayah_start']}-{video['ayah_end']}\n\nTranscript:\n{transcript}"
    )
    last_error = None
    for attempt in range(1, 4):
        try:
            generated = call_azure(prompt, message, max_tokens=4000)
            break
        except Exception as exc:
            last_error = exc
            if attempt < 3:
                time.sleep(attempt * 3)
    else:
        range_label = str(video["ayah_start"])
        if video["ayah_end"] != video["ayah_start"]:
            range_label += f"–{video['ayah_end']}"
        generated = {
            "title": f"{config['name']} {range_label}: Kaynak tefsir anlatımı",
            "description": (
                f"{config['name']} sûresinin {range_label}. ayetlerini ele alan kaynak tefsir anlatımı. "
                "Video transkripti; ayetlerin açıklamasını, aktarılan görüşleri ve konuşma içindeki örnekleri korur."
            ),
            "tags": [
                f"{config['name']} tefsiri",
                f"{config['name']} {range_label}",
                "Kur’an tefsiri",
                "ayet açıklaması",
                "180 Saniyede Tefsir",
            ],
            "type": "normal",
            "playlists": [f"{config['name']} Suresi Tefsiri", "180 Saniyede Tefsir"],
            "generation_note": f"Deterministic fallback after metadata model error: {last_error}",
        }
    generated_path.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return video["id"], generated


def load_database(videos: list[dict], config: dict) -> None:
    rest = local_rest()
    names = canonical_names(videos, config)
    prompt = (ROOT / "prompts/youtube-description.md").read_text(encoding="utf-8")
    descriptions: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(description_for, video, config, prompt): video for video in videos}
        for index, future in enumerate(as_completed(futures), start=1):
            video_id, generated = future.result()
            descriptions[video_id] = generated
            print(f"[{index}/{len(videos)}] described {video_id}", flush=True)

    now = datetime.now(timezone.utc).isoformat()
    for index, video in enumerate(videos, start=1):
        target = AUDIO / config["key"] / video["id"]
        info = json.loads((target / "source.info.json").read_text(encoding="utf-8"))
        transcript = (target / "transcript.txt").read_text(encoding="utf-8").strip()
        linked = rest.get(
            "media_sources",
            "select=media_transcription_id&platform=eq.youtube&external_id=eq." + video["id"],
        )
        payload = {
            "file_name": names[video["id"]],
            "type": "youtube",
            "transcription": transcript,
            "description": render_description(descriptions[video["id"]]),
            "status": "described",
            "surah_key": config["key"],
            "surah_name": config["name"],
            "surah_number": config["number"],
            "updated_at": now,
        }
        if linked and linked[0].get("media_transcription_id"):
            row_id = linked[0]["media_transcription_id"]
            rest.patch("media_transcriptions", f"id=eq.{row_id}", payload)
        else:
            created = rest.post(
                "media_transcriptions",
                {**payload, "created_at": now},
                representation=True,
            )
            row_id = created[0]["id"]
        origin = target / "transcript.origin.txt"
        if not origin.exists():
            origin.write_text("youtube_auto_captions\n", encoding="utf-8")
        upsert_source(rest, row_id, video, info)
        print(f"[{index}/{len(videos)}] loaded {names[video['id']]}", flush=True)


def audit(config: dict) -> dict:
    rest = local_rest()
    rows = rest.get(
        "media_transcriptions",
        f"select=id,file_name,transcription,description,status&surah_key=eq.{config['key']}&order=id.asc",
    )
    sources = rest.get(
        "media_sources",
        f"select=id,ayah_start,ayah_end,external_id&surah_key=eq.{config['key']}&order=ayah_start.asc",
    )
    coverage = set()
    for source in sources:
        coverage.update(range(source["ayah_start"], source["ayah_end"] + 1))
    missing_ayahs = sorted(set(range(1, config["ayah_count"] + 1)) - coverage)
    report = {
        "surah": config["name"],
        "rows": len(rows),
        "source_links": len(sources),
        "covered_ayahs": len(coverage),
        "missing_ayahs": missing_ayahs,
        "allowed_channel_gaps": config.get("allowed_missing_ayahs", []),
        "unexpected_missing_ayahs": sorted(set(missing_ayahs) - set(config.get("allowed_missing_ayahs", []))),
        "missing_transcriptions": [row["file_name"] for row in rows if not (row.get("transcription") or "").strip()],
        "missing_descriptions": [row["file_name"] for row in rows if not (row.get("description") or "").strip()],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("surah", choices=sorted(SURAHS))
    parser.add_argument("command", choices=["discover", "source", "load", "audit", "all"], default="all", nargs="?")
    args = parser.parse_args()
    config = SURAHS[args.surah]
    videos = discover(config)
    validate_inventory(videos, config)
    if args.command in {"source", "all"}:
        source_all(videos, config)
    if args.command in {"load", "all"}:
        load_database(videos, config)
    if args.command in {"audit", "all"}:
        report = audit(config)
        if report["unexpected_missing_ayahs"] or report["missing_transcriptions"] or report["missing_descriptions"]:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
