#!/usr/bin/env python3
from faster_whisper import WhisperModel
import json
from pathlib import Path
import sys

model = WhisperModel("base", device="cpu", compute_type="int8")


def run(audio: str) -> str:
    segments, _ = model.transcribe(audio, language="tr", beam_size=5, vad_filter=True)
    return " ".join(segment.text.strip() for segment in segments if segment.text.strip())


if len(sys.argv) == 3 and sys.argv[1] == "--batch":
    jobs = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    for index, job in enumerate(jobs, start=1):
        output = Path(job["transcript"])
        if not output.exists():
            output.write_text(run(job["audio"]).strip() + "\n", encoding="utf-8")
        print(f"[{index}/{len(jobs)}] {output.name}", flush=True)
else:
    print(run(sys.argv[1]))
