# Pipeline

The scripts read existing credentials from `~/.openclaw/.env`; secrets are
never copied into this project.

```bash
npm run db:start
python3 scripts/pipeline.py all
npm run prose:build
npm install
npm run review
```

To ingest or refresh the complete En‘âm collection:

```bash
python3 scripts/ingest_surah.py enam all
npm run prose:build
```

The En‘âm inventory contains 120 source videos covering all 165 ayahs. Caption,
metadata, generated-description, and prose outputs are cached, so every stage is
safe to resume.

The same resumable pipeline supports the channel's older collections:

```bash
npm run surah:ali-imran
npm run surah:nisa
npm run surah:maide
```

Run all three sequentially with:

```bash
npm run surahs:populate
```

Every import performs five stages: channel discovery, title/range parsing,
coverage validation, Turkish-caption acquisition with speech-to-text fallback,
and local Supabase insertion with source provenance. Existing external YouTube
IDs are updated rather than duplicated. Cached captions, metadata, and generated
descriptions make interrupted imports safe to rerun.

Current channel inventories:

- Âl-i İmrân: 31 videos covering ayahs 3–200. The channel has no titled source
  video for ayahs 1–2; this is recorded as an allowed channel gap.
- Nisâ: 24 videos covering all 176 ayahs. The known `18` typo in the title of
  the 163–170 video is explicitly corrected during range parsing.
- Mâide: 28 videos covering all 120 ayahs, including overlapping focused videos
  for the opening ayahs.

Audit imported rows at any time:

```bash
npm run surahs:audit
```

Individual stages are also available:

```bash
python3 scripts/pipeline.py sync
python3 scripts/pipeline.py discover
python3 scripts/pipeline.py link
python3 scripts/pipeline.py complete
python3 scripts/pipeline.py audit
```

`sync` only reads the hosted Supabase project. All inserts, transcription work,
and generated descriptions go to the local project.

`npm run prose:build` converts every supported YouTube transcript to lightly
edited written prose, validates the replacement multi-sûra vault, archives the
current vault, and activates the new one.
