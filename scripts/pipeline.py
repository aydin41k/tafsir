#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
AUDIO = DATA / "audio"
CHANNEL_URL = "https://www.youtube.com/@180saniyedetefsir/videos"
TRANSCRIBE_PY = Path.home() / ".openclaw/workspace/.venv/transcribe/bin/python"


def load_private_env() -> dict[str, str]:
    env = dict(os.environ)
    path = Path.home() / ".openclaw/.env"
    if path.exists():
        for raw in path.read_text(encoding="utf-8").splitlines():
            raw = raw.strip()
            if not raw or raw.startswith("#") or "=" not in raw:
                continue
            key, value = raw.split("=", 1)
            env.setdefault(key.strip(), value.strip().strip("\"'"))
    return env


def local_credentials() -> tuple[str, str]:
    output = subprocess.check_output(
        ["npx", "--yes", "supabase@latest", "status", "-o", "env"],
        cwd=ROOT,
        text=True,
        stderr=subprocess.STDOUT,
    )
    values: dict[str, str] = {}
    for line in output.splitlines():
        match = re.match(r"^([A-Z_]+)=(.*)$", line.strip())
        if match:
            values[match.group(1)] = match.group(2).strip().strip("\"'")
    url = values.get("API_URL") or values.get("SUPABASE_URL")
    key = values.get("SERVICE_ROLE_KEY") or values.get("SERVICE_ROLE_JWT")
    if not key:
        names = subprocess.check_output(
            ["docker", "ps", "--format", "{{.Names}}"], text=True
        ).splitlines()
        kong = next((name for name in names if name.startswith("supabase_kong_")), None)
        if kong:
            bootstrap = subprocess.check_output(
                ["docker", "inspect", kong, "--format", "{{index .Config.Entrypoint 2}}"],
                text=True,
            )
            match = re.search(r"apikey == '(sb_secret_[^']+)'", bootstrap)
            if match:
                key = match.group(1)
    if not url or not key:
        raise RuntimeError("Could not read local Supabase API credentials")
    return url.rstrip("/"), key


def http_json(method: str, url: str, headers: dict[str, str], payload=None, timeout=180):
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8")
    return json.loads(body) if body else None


class Rest:
    def __init__(self, url: str, key: str):
        self.url = url.rstrip("/")
        self.headers = {"apikey": key, "Authorization": f"Bearer {key}"}

    def get(self, table: str, query: str = ""):
        return http_json("GET", f"{self.url}/rest/v1/{table}?{query}", self.headers) or []

    def post(self, table: str, rows, representation: bool = False):
        headers = {**self.headers, "Content-Type": "application/json"}
        headers["Prefer"] = "return=representation" if representation else "return=minimal"
        return http_json("POST", f"{self.url}/rest/v1/{table}", headers, rows)

    def patch(self, table: str, query: str, payload):
        headers = {**self.headers, "Content-Type": "application/json", "Prefer": "return=representation"}
        return http_json("PATCH", f"{self.url}/rest/v1/{table}?{query}", headers, payload) or []

    def delete(self, table: str, query: str):
        headers = {**self.headers, "Prefer": "return=minimal"}
        return http_json("DELETE", f"{self.url}/rest/v1/{table}?{query}", headers)


def remote_rest() -> Rest:
    env = load_private_env()
    return Rest(env["SUPABASE_URL"], env["SUPABASE_API_KEY"])


def local_rest() -> Rest:
    return Rest(*local_credentials())


def sync_remote() -> None:
    remote = remote_rest()
    local = local_rest()
    rows = remote.get("media_transcriptions", "select=*&order=id.asc")
    local.delete("media_sources", "id=gt.0")
    local.delete("media_transcriptions", "id=gt.0")
    copied = []
    for row in rows:
        copy = {key: value for key, value in row.items() if key != "id"}
        copied.append(copy)
    for offset in range(0, len(copied), 20):
        local.post("media_transcriptions", copied[offset:offset + 20])
    print(json.dumps({"synced_rows": len(copied)}, ensure_ascii=False))


def ascii_fold(value: str) -> str:
    value = value.replace("ı", "i").replace("İ", "I")
    return "".join(
        char for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    ).lower()


def normalize_araf(value: str) -> str:
    return re.sub(r"a[^a-z0-9]?raf", "araf", ascii_fold(value))


def parse_ayah_range(value: str) -> tuple[int, int] | None:
    folded = normalize_araf(value)
    match = re.search(r"araf[^0-9]{0,20}(\d{1,3})(?:\s*[-–]\s*(\d{1,3}))?", folded)
    if not match:
        return None
    start = int(match.group(1))
    end = int(match.group(2) or start)
    if end == start:
        adjacent = re.search(r"araf\s+(\d{1,3})\s+(\d{1,3})(?:\s|$)", folded)
        if adjacent and int(adjacent.group(1)) == start:
            end = int(adjacent.group(2))
    if not (1 <= start <= end <= 206):
        return None
    return start, end


def is_primary_tefsir_video(title: str) -> bool:
    folded = normalize_araf(title)
    return folded.startswith("araf") and (
        "[tefsir]" in folded or "suresi" in folded or re.match(r"^araf\s+\d", folded)
    )


def discover_channel() -> list[dict]:
    raw = subprocess.check_output(
        ["yt-dlp", "--js-runtimes", "node", "--flat-playlist", "--dump-single-json", CHANNEL_URL],
        text=True,
    )
    channel = json.loads(raw)
    videos = []
    for item in channel.get("entries") or []:
        title = item.get("title") or ""
        ayahs = parse_ayah_range(title)
        if ayahs and is_primary_tefsir_video(title):
            videos.append({
                "id": item["id"],
                "title": title,
                "url": item.get("url") or f"https://www.youtube.com/watch?v={item['id']}",
                "duration": item.get("duration"),
                "ayah_start": ayahs[0],
                "ayah_end": ayahs[1],
            })
    videos.sort(key=lambda item: (item["ayah_start"], item["ayah_end"], item["title"]))
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "channel-araf.json").write_text(
        json.dumps(videos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"araf_primary_videos": len(videos)}, ensure_ascii=False))
    return videos


def row_range(row: dict) -> tuple[int, int] | None:
    return parse_ayah_range(row.get("file_name") or "")


def canonical_file_names(videos: list[dict]) -> dict[str, str]:
    counts = Counter((item["ayah_start"], item["ayah_end"]) for item in videos)
    names = {}
    for item in videos:
        start, end = item["ayah_start"], item["ayah_end"]
        verse = str(start) if start == end else f"{start}-{end}"
        suffix = f" - {item['id']}" if counts[(start, end)] > 1 else ""
        names[item["id"]] = f"Araf {verse}{suffix}.mp3"
    return names


def choose_video_for_row(row: dict, videos: list[dict], used: set[str]) -> dict | None:
    target = row_range(row)
    if not target:
        return None
    candidates = [
        video for video in videos
        if (video["ayah_start"], video["ayah_end"]) == target and video["id"] not in used
    ]
    if not candidates:
        return None
    candidates.sort(key=lambda item: (
        0 if "[tefsir]" in normalize_araf(item["title"]) else 1,
        0 if "suresi" in normalize_araf(item["title"]) else 1,
        item["title"],
    ))
    part = re.search(r"\((\d+)\)", row.get("file_name") or "")
    if part:
        marker = f"({part.group(1)}. bolum)"
        for candidate in candidates:
            if marker in ascii_fold(candidate["title"]):
                return candidate
    return candidates[0]


def transcript_from_json3(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    chunks = []
    for event in payload.get("events") or []:
        text = "".join(segment.get("utf8") or "" for segment in event.get("segs") or [])
        text = re.sub(r"\s+", " ", text).strip()
        if text and (not chunks or chunks[-1] != text):
            chunks.append(text)
    return " ".join(chunks)


def download_auto_captions(video: dict, target_dir: Path) -> bool:
    subprocess.check_call([
        "yt-dlp", "--quiet", "--no-warnings", "--js-runtimes", "node", "--write-auto-subs",
        "--sub-langs", "tr-orig", "--sub-format", "json3", "--skip-download",
        "--write-info-json", "--no-write-playlist-metafiles",
        "-o", str(target_dir / "source.%(ext)s"), video["url"],
    ])
    caption = target_dir / "source.tr-orig.json3"
    if not caption.exists():
        return False
    (target_dir / "transcript.txt").write_text(transcript_from_json3(caption) + "\n", encoding="utf-8")
    (target_dir / "transcript.origin.txt").write_text("youtube_auto_captions\n", encoding="utf-8")
    return True


def fetch_full_metadata(video: dict, target_dir: Path, download: bool) -> dict:
    target_dir.mkdir(parents=True, exist_ok=True)
    info_path = target_dir / "source.info.json"
    audio_path = target_dir / "source.mp3"
    transcript_path = target_dir / "transcript.txt"
    if download and not transcript_path.exists():
        try:
            if download_auto_captions(video, target_dir):
                pass
            else:
                raise RuntimeError("Turkish original captions were not available")
        except subprocess.CalledProcessError:
            pass
        except RuntimeError:
            pass
    if download and not transcript_path.exists() and not audio_path.exists():
        subprocess.check_call([
            "yt-dlp", "--quiet", "--no-warnings", "--js-runtimes", "node", "-x", "--audio-format", "mp3", "--audio-quality", "0",
            "--write-info-json", "--no-write-playlist-metafiles",
            "-o", str(target_dir / "source.%(ext)s"), video["url"],
        ])
    if not info_path.exists():
        raw = subprocess.check_output(["yt-dlp", "--quiet", "--no-warnings", "--js-runtimes", "node", "--dump-single-json", video["url"]], text=True)
        info_path.write_text(raw, encoding="utf-8")
    return json.loads(info_path.read_text(encoding="utf-8"))


def iso_upload_date(info: dict) -> str | None:
    stamp = info.get("timestamp") or info.get("release_timestamp")
    if stamp:
        return datetime.fromtimestamp(stamp, timezone.utc).isoformat()
    value = info.get("upload_date")
    if value and len(value) == 8:
        return f"{value[:4]}-{value[4:6]}-{value[6:]}T00:00:00+00:00"
    return None


def upsert_source(local: Rest, row_id: int, video: dict, info: dict) -> None:
    existing = local.get("media_sources", "select=id&platform=eq.youtube&external_id=eq." + video["id"])
    nested_origin = AUDIO / video.get("surah_key", "") / video["id"] / "transcript.origin.txt"
    legacy_origin = AUDIO / video["id"] / "transcript.origin.txt"
    origin_path = nested_origin if nested_origin.exists() else legacy_origin
    payload = {
        "media_transcription_id": row_id,
        "platform": "youtube",
        "external_id": video["id"],
        "source_url": video["url"],
        "title": info.get("title") or video["title"],
        "surah_key": video.get("surah_key", "araf"),
        "surah_name": video.get("surah_name", "A‘râf"),
        "surah_number": video.get("surah_number", 7),
        "published_at": iso_upload_date(info),
        "duration_seconds": int(info.get("duration") or video.get("duration") or 0),
        "ayah_start": video["ayah_start"],
        "ayah_end": video["ayah_end"],
        "part_label": None,
        "metadata": {
            "channel": info.get("channel"),
            "channel_id": info.get("channel_id"),
            "original_description": info.get("description") or "",
            "thumbnail": info.get("thumbnail"),
            "webpage_url": info.get("webpage_url") or video["url"],
            "transcript_origin": (
                origin_path.read_text(encoding="utf-8").strip()
                if origin_path.exists()
                else "local_faster_whisper"
            ),
        },
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    if existing:
        local.patch("media_sources", f"id=eq.{existing[0]['id']}", payload)
    else:
        local.post("media_sources", payload)


def link_existing_sources(videos: list[dict]) -> None:
    local = local_rest()
    rows = local.get("media_transcriptions", "select=*&type=eq.youtube&order=id.asc")
    used: set[str] = set()
    linked = 0
    for row in rows:
        video = choose_video_for_row(row, videos, used)
        if not video:
            continue
        # The hosted table already contains the description and transcript for
        # these rows. Flat-playlist metadata is enough to establish stable
        # provenance without making one extra YouTube request per video.
        info = {
            "id": video["id"],
            "title": video["title"],
            "duration": video.get("duration"),
            "webpage_url": video["url"],
        }
        upsert_source(local, row["id"], video, info)
        used.add(video["id"])
        linked += 1
    print(json.dumps({"linked_existing_sources": linked}, ensure_ascii=False))


def transcribe(audio_path: Path, transcript_path: Path) -> str:
    if transcript_path.exists():
        return transcript_path.read_text(encoding="utf-8").strip()
    if not TRANSCRIBE_PY.exists():
        raise RuntimeError(f"Missing existing faster-whisper environment: {TRANSCRIBE_PY}")
    helper = ROOT / "scripts/transcribe_helper.py"
    output = subprocess.check_output([str(TRANSCRIBE_PY), str(helper), str(audio_path)], text=True)
    transcript_path.write_text(output.strip() + "\n", encoding="utf-8")
    return output.strip()


def call_azure(prompt: str, user_message: str, max_tokens: int = 5000, model: str | None = None) -> dict:
    env = load_private_env()
    url = env["AZURE_OPENAI_BASE_URL"].rstrip("/") + "/chat/completions"
    payload = {
        "model": model or env.get("YOUTUBE_DESCRIBE_MODEL", "gpt-5.5"),
        "max_completion_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message},
        ],
        "response_format": {"type": "json_object"},
    }
    headers = {"api-key": env["AZURE_OPENAI_API_KEY"], "Content-Type": "application/json"}
    try:
        response = http_json("POST", url, headers, payload, timeout=300)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        if exc.code != 400 or "response_format" not in body:
            raise
        payload.pop("response_format", None)
        response = http_json("POST", url, headers, payload, timeout=300)
    content = response["choices"][0]["message"]["content"].strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content, flags=re.S)
    return json.loads(content)


def render_description(metadata: dict) -> str:
    description = str(metadata.get("description") or "").strip()
    tags = [str(tag).strip().lstrip("#") for tag in metadata.get("tags") or [] if str(tag).strip()]
    return description + (("\n\n---\n" + ", ".join(tags)) if tags else "")


def prepare_early_videos(videos: list[dict]) -> None:
    early = [video for video in videos if video["ayah_end"] <= 64]
    prompt = (ROOT / "prompts/youtube-description.md").read_text(encoding="utf-8")
    jobs = []
    infos: dict[str, dict] = {}
    def prepare_source(video: dict) -> tuple[dict, dict]:
        target = AUDIO / video["id"]
        info = fetch_full_metadata(video, target, download=True)
        return video, info

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(prepare_source, video): video for video in early}
        finished = 0
        for future in as_completed(futures):
            video, info = future.result()
            infos[video["id"]] = info
            finished += 1
            print(f"[{finished}/{len(early)}] sourced {video['title']}", flush=True)

    for video in early:
        target = AUDIO / video["id"]
        transcript_path = target / "transcript.txt"
        if not transcript_path.exists() and (target / "source.mp3").exists():
            jobs.append({"audio": str(target / "source.mp3"), "transcript": str(transcript_path)})
    if jobs:
        manifest = DATA / "transcribe-manifest.json"
        manifest.write_text(json.dumps(jobs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        subprocess.check_call([str(TRANSCRIBE_PY), str(ROOT / "scripts/transcribe_helper.py"), "--batch", str(manifest)])
        for job in jobs:
            Path(job["transcript"]).with_name("transcript.origin.txt").write_text("local_faster_whisper\n", encoding="utf-8")
    def describe_source(video: dict) -> str:
        target = AUDIO / video["id"]
        generated_path = target / "description.generated.json"
        if not generated_path.exists():
            transcript = (target / "transcript.txt").read_text(encoding="utf-8").strip()
            generated = call_azure(
                prompt,
                f"Source video: {infos[video['id']].get('title') or video['title']}\n"
                f"A‘râf {video['ayah_start']}-{video['ayah_end']}\n\nTranscript:\n{transcript}",
            )
            generated_path.write_text(
                json.dumps(generated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        return video["title"]

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(describe_source, video) for video in early]
        for index, future in enumerate(as_completed(futures), start=1):
            print(f"[{index}/{len(early)}] described {future.result()}", flush=True)
    print(json.dumps({"prepared_early_videos": len(early)}, ensure_ascii=False))


def complete_early_videos(videos: list[dict]) -> None:
    local = local_rest()
    early = [video for video in videos if video["ayah_end"] <= 64]
    names = canonical_file_names(early)
    prompt = (ROOT / "prompts/youtube-description.md").read_text(encoding="utf-8")
    completed = 0
    for index, video in enumerate(early, start=1):
        file_name = names[video["id"]]
        existing = local.get(
            "media_transcriptions",
            "select=*&type=eq.youtube&file_name=eq." + urllib.parse.quote(file_name, safe=""),
        )
        target = AUDIO / video["id"]
        info = fetch_full_metadata(video, target, download=True)
        transcript = transcribe(target / "source.mp3", target / "transcript.txt")
        now = datetime.now(timezone.utc).isoformat()
        if existing:
            row = existing[0]
            local.patch("media_transcriptions", f"id=eq.{row['id']}", {
                "transcription": transcript, "status": row.get("status") or "transcribed", "updated_at": now,
            })
        else:
            created = local.post("media_transcriptions", {
                "file_name": file_name,
                "type": "youtube",
                "transcription": transcript,
                "status": "transcribed",
                "created_at": now,
                "updated_at": now,
            }, representation=True)
            row = created[0]
        generated_path = target / "description.generated.json"
        if generated_path.exists():
            generated = json.loads(generated_path.read_text(encoding="utf-8"))
        else:
            generated = call_azure(
                prompt,
                f"Source video: {info.get('title') or video['title']}\n"
                f"A‘râf {video['ayah_start']}-{video['ayah_end']}\n\nTranscript:\n{transcript}",
            )
            generated_path.write_text(
                json.dumps(generated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        local.patch("media_transcriptions", f"id=eq.{row['id']}", {
            "description": render_description(generated),
            "status": "described",
            "updated_at": datetime.now(timezone.utc).isoformat(),
        })
        upsert_source(local, row["id"], video, info)
        completed += 1
        print(f"[{index}/{len(early)}] completed {file_name}", flush=True)
    print(json.dumps({"completed_early_videos": completed}, ensure_ascii=False))


def audit() -> None:
    local = local_rest()
    rows = local.get("media_transcriptions", "select=*&order=id.asc")
    sources = local.get("media_sources", "select=*&order=ayah_start.asc")
    araf_rows = [row for row in rows if row_range(row)]
    coverage = set()
    for row in araf_rows:
        start, end = row_range(row) or (0, -1)
        if row.get("type") == "youtube":
            coverage.update(range(start, end + 1))
    print(json.dumps({
        "local_rows": len(rows),
        "araf_rows": len(araf_rows),
        "source_links": len(sources),
        "covered_ayahs": len(coverage),
        "missing_ayahs": [ayah for ayah in range(1, 207) if ayah not in coverage],
        "missing_transcriptions": [row["file_name"] for row in araf_rows if not (row.get("transcription") or "").strip()],
        "missing_descriptions": [row["file_name"] for row in araf_rows if not (row.get("description") or "").strip()],
    }, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["sync", "discover", "prepare", "link", "complete", "audit", "all"])
    args = parser.parse_args()
    videos = None
    if args.command in {"sync", "all"}:
        sync_remote()
    if args.command in {"discover", "prepare", "link", "complete", "all"}:
        videos = discover_channel()
    if args.command in {"prepare", "all"}:
        prepare_early_videos(videos or [])
    if args.command in {"link", "all"}:
        link_existing_sources(videos or [])
    if args.command in {"complete", "all"}:
        complete_early_videos(videos or [])
    if args.command in {"audit", "all"}:
        audit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
