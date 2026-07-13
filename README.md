# Yazılı Tefsir Kütüphanesi

Live site: https://tafsir.salimov.site

A public, source-traceable reading edition of five **180 Saniyede Tefsir**
video collections: Âl-i İmrân, Nisâ, Mâide, En‘âm, and A‘râf. The canonical
articles are lightly edited transcripts, not summaries or new interpretations.

The public site includes:

- 867 ayah pages and 331 full written tefsir texts across five sûra collections
- An explicit source-gap notice for Âl-i İmrân 1–2, for which no matching channel video was found
- Direct links from every edited text to its untouched transcript
- Full-library search with `⌘/Ctrl K` and `/` shortcuts
- Desktop reading navigation, mobile drawer, and contextual table of contents
- Light/dark themes, reading progress, and continue-reading state
- Responsive editorial typography and accessible keyboard interactions
- Friendly URLs, canonical metadata, JSON-LD, sitemap, robots, and health check
- No database dependency at runtime; the Markdown vault ships with the app

## Run locally

Requires Node.js 22 or later.

```bash
npm install
npm start
```

Open `http://127.0.0.1:4173`.

Useful checks:

```bash
npm run check
npm run test:ui
```

The browser tests require Chromium. Install it once with:

```bash
npx playwright install chromium
```

## Production deployment

Pull requests and pushes to `main` run the static and browser test suites in
GitHub Actions. After a tested commit reaches `main`, the `Deploy production`
job installs production dependencies on the Namecheap server, updates the
Passenger application, restarts it, and verifies the public health endpoint.

The deploy job uses the protected GitHub environment `prod` and its
`NAMECHEAP_SSH_KEY` secret. Production deployments therefore only run from
`main`; pull requests never receive the server key.

## Public routes

- `/` — Markdown wiki index
- `/sure/ali-imran`, `/sure/nisa`, `/sure/maide`, `/sure/enam`, and `/sure/araf` — per-sûra ayah explorers
- `/sure/:surah/ayet/:number` — one ayah and its narrowest applicable source texts
- `/metinler` — provenance archive for the source texts embedded in ayah pages
- `/metin/:id` — one lightly edited source article
- `/transkript/:id` — the corresponding untouched transcript
- `/wiki/Metodoloji` — editorial method
- `/api/search?q=...` — search API
- `/healthz` — deployment health check
- `/sitemap.xml` and `/robots.txt` — crawler discovery

## Environment variables

Copy `.env.example` as a reference. The server reads:

| Variable | Default | Purpose |
|---|---|---|
| `PORT` | `4173` | HTTP port; hosting providers usually set this automatically |
| `HOST` | `0.0.0.0` | Bind address |
| `SITE_URL` | Request origin | Public canonical origin, for example `https://araf.example.com` |
| `NODE_ENV` | — | Set to `production` to enable longer static-asset caching |

Set `SITE_URL` in production so canonical URLs, Open Graph metadata, robots, and
the sitemap use the final domain.

## Deploy with Docker

```bash
docker build -t araf-wiki .
docker run --rm -p 4173:4173 \
  -e SITE_URL=https://your-domain.example \
  araf-wiki
```

The image installs production dependencies only and contains `site/` plus the
complete `vault/`. It does not require Supabase, PostgreSQL, or persistent disk.

## Deploy to Render

1. Push this directory to a Git repository.
2. In Render, create a Blueprint from the repository. `render.yaml` defines the
   Docker service and `/healthz` check.
3. Set `SITE_URL` to the final Render or custom-domain URL.
4. Deploy.

## Deploy to Railway

1. Create a Railway project from the Git repository.
2. Railway reads `railway.json` and builds the included Dockerfile.
3. Set `SITE_URL` to the generated or custom-domain URL.
4. Deploy and confirm `/healthz` returns `{ "ok": true, ... }`.

## Content architecture

- `vault/Ham-Transkriptler/` — untouched database transcripts
- `vault/Tefsir-Metinleri/` — very lightly edited written versions
- `vault/Ayetler/` — per-sûra ayah pages embedding the narrowest applicable texts
- `data/` — source metadata and cached processing output
- `site/` — public Express application and frontend assets
- `scripts/` — transcription, editing, audit, and vault-build pipeline
- `archive/` — preserved previous synthesis-based vault

The local `media_transcriptions` replica and Supabase tooling remain available
for pipeline work, but they are deliberately outside the public runtime.

See `scripts/README.md` for ingestion and rebuild commands.

Use `npm run surahs:populate` to refresh the Âl-i İmrân, Nisâ, and Mâide
imports and `npm run surahs:audit` to verify coverage and required fields.
