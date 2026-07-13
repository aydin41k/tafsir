import compression from "compression";
import express from "express";
import matter from "gray-matter";
import MarkdownIt from "markdown-it";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const VAULT = path.join(ROOT, "vault");
const ASSETS = path.join(HERE, "assets");
const PORT = Number(process.env.PORT || 4173);
const HOST = process.env.HOST || "0.0.0.0";
const configuredBasePath = String(process.env.BASE_PATH || "").trim();
const BASE_PATH = configuredBasePath && configuredBasePath !== "/"
  ? `/${configuredBasePath.replace(/^\/+|\/+$/g, "")}`
  : "";
const SITE_NAME = "Yazılı Tefsir Kütüphanesi";
const DEFAULT_DESCRIPTION = "180 Saniyede Tefsir video transkriptlerinden hazırlanmış, kaynağa sadık Âl-i İmrân, Nisâ, Mâide, En‘âm ve A‘râf yazılı tefsirlerini okuyun.";
const SURAHS = {
  "ali-imran": { key: "ali-imran", name: "Âl-i İmrân", number: 3, ayahCount: 200, mark: "٣", description: "İman, vahiy, Ehl-i kitap, Meryem ve Uhud etrafındaki anlatımlar." },
  nisa: { key: "nisa", name: "Nisâ", number: 4, ayahCount: 176, mark: "٤", description: "Aile, adalet, haklar ve toplum düzeni etrafındaki anlatımlar." },
  maide: { key: "maide", name: "Mâide", number: 5, ayahCount: 120, mark: "٥", description: "Ahitler, helâl-haram, şahitlik ve sorumluluk etrafındaki anlatımlar." },
  enam: { key: "enam", name: "En‘âm", number: 6, ayahCount: 165, mark: "٦", description: "Tevhid, vahiy, peygamberlik ve şirk eleştirisi etrafındaki anlatımlar." },
  araf: { key: "araf", name: "A‘râf", number: 7, ayahCount: 206, mark: "٧", description: "İnsanlık kıssaları, kulluk, ahlak ve ilahî hitap etrafındaki anlatımlar." },
};

const app = express();
app.disable("x-powered-by");
app.use((req, _res, next) => {
  if (BASE_PATH && (req.url === BASE_PATH || req.url.startsWith(`${BASE_PATH}/`))) {
    req.url = req.url.slice(BASE_PATH.length) || "/";
  }
  next();
});
app.use(compression());
app.use((_req, res, next) => {
  res.set({
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Cross-Origin-Opener-Policy": "same-origin",
  });
  next();
});
app.use("/assets", express.static(ASSETS, { maxAge: process.env.NODE_ENV === "production" ? "7d" : 0 }));

const md = new MarkdownIt({ html: true, linkify: true, typographer: true });
const defaultLinkOpen = md.renderer.rules.link_open || ((tokens, idx, options, _env, self) => self.renderToken(tokens, idx, options));
md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
  const href = tokens[idx].attrGet("href") || "";
  if (/^https?:\/\//.test(href)) {
    tokens[idx].attrSet("target", "_blank");
    tokens[idx].attrSet("rel", "noopener noreferrer");
  }
  return defaultLinkOpen(tokens, idx, options, env, self);
};
md.renderer.rules.heading_open = (tokens, idx, options, _env, self) => {
  const title = tokens[idx + 1]?.content || "";
  tokens[idx].attrSet("id", slugify(title));
  return self.renderToken(tokens, idx, options);
};

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function publicPath(value = "/") {
  const pathValue = value.startsWith("/") ? value : `/${value}`;
  return pathValue === "/" ? `${BASE_PATH}/` : `${BASE_PATH}${pathValue}`;
}

function prefixInternalUrls(html) {
  if (!BASE_PATH) return html;
  return html.replace(/\b(href|src)="\/(?!\/)/g, `$1="${BASE_PATH}/`);
}

function slugify(value = "") {
  return String(value)
    .toLocaleLowerCase("tr")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/ı/g, "i")
    .replace(/[^a-z0-9çğöşü]+/g, "-")
    .replace(/^-|-$/g, "");
}

function normalize(value = "") {
  return String(value)
    .toLocaleLowerCase("tr")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/ı/g, "i");
}

function stripMarkdown(value = "") {
  return String(value)
    .replace(/^---\s*\n[\s\S]*?\n---\s*\n?/, "")
    .replace(/<details>[\s\S]*?<\/details>/gi, "")
    .replace(/^>\s*\[![^\]]+\]\s*/gm, "")
    .replace(/!?\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (_match, target, label) => label || target)
    .replace(/<[^>]+>/g, " ")
    .replace(/[#>*_`~|\[\]()]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function walk(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    if (entry.name.startsWith(".")) return [];
    return entry.isDirectory() ? walk(full) : entry.name.endsWith(".md") ? [full] : [];
  });
}

function readingMinutes(content = "") {
  const words = stripMarkdown(content).split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / 210));
}

function surahFor(page) {
  const key = String(page?.data?.surah_key || "").toLowerCase();
  if (SURAHS[key]) return SURAHS[key];
  const name = normalize(page?.data?.surah || page?.title || "");
  if (name.includes("ali-imran") || name.includes("ali imran")) return SURAHS["ali-imran"];
  if (name.includes("nisa")) return SURAHS.nisa;
  if (name.includes("maide")) return SURAHS.maide;
  if (name.includes("enam")) return SURAHS.enam;
  return SURAHS.araf;
}

function formatRange(page) {
  const start = Number(page?.data?.ayah_start || page?.data?.ayah || 0);
  const end = Number(page?.data?.ayah_end || start);
  if (!start) return "";
  return `${surahFor(page).name} ${start}${end !== start ? `–${end}` : ""}`;
}

function pageTypeLabel(type) {
  return {
    ayah: "Ayet",
    "tefsir-text": "Yazılı tefsir",
    "raw-transcript": "Ham transkript",
    surah: "Sûre haritası",
    index: "İndeks",
    methodology: "Metodoloji",
    dashboard: "İnceleme",
  }[type] || "Not";
}

function loadContent() {
  const pages = walk(VAULT).map((file) => {
    const relative = path.relative(VAULT, file).replaceAll(path.sep, "/").replace(/\.md$/, "");
    const parsed = matter(fs.readFileSync(file, "utf8"));
    const page = {
      file,
      relative,
      stem: path.basename(relative),
      title: parsed.data.title || path.basename(relative),
      type: parsed.data.type || "note",
      content: parsed.content,
      data: parsed.data,
    };
    page.plain = stripMarkdown(parsed.content);
    page.excerpt = page.plain.slice(0, 230) + (page.plain.length > 230 ? "…" : "");
    page.readingMinutes = readingMinutes(parsed.content);
    return page;
  });

  const lookup = new Map();
  const ayahs = new Map();
  const surahs = new Map();
  const articles = new Map();
  const transcripts = new Map();
  for (const page of pages) {
    lookup.set(page.relative.toLowerCase(), page);
    lookup.set(page.stem.toLowerCase(), page);
    lookup.set(page.title.toLocaleLowerCase("tr"), page);
    if (page.type === "ayah") ayahs.set(`${surahFor(page).key}:${Number(page.data.ayah)}`, page);
    if (page.type === "surah") surahs.set(surahFor(page).key, page);
    if (page.type === "tefsir-text") articles.set(Number(page.data.row_id), page);
    if (page.type === "raw-transcript") transcripts.set(Number(page.data.row_id), page);
  }

  const textArticles = pages
    .filter((page) => page.type === "tefsir-text")
    .sort((a, b) => surahFor(a).number - surahFor(b).number || Number(a.data.ayah_start) - Number(b.data.ayah_start) || Number(a.data.ayah_end) - Number(b.data.ayah_end) || a.title.localeCompare(b.title, "tr"));

  function search(query, limit = 18) {
    const q = normalize(query).trim();
    if (q.length < 2) return [];
    const tokens = q.split(/\s+/).filter(Boolean);
    const includeRaw = /ham|transkript|kaynak/.test(q);
    const ranked = pages
      .filter((page) => includeRaw || page.type !== "raw-transcript")
      .map((page) => {
        const title = normalize(page.title);
        const range = normalize(formatRange(page));
        const body = normalize(page.plain);
        let score = 0;
        if (title === q) score += 120;
        if (title.startsWith(q)) score += 70;
        if (title.includes(q)) score += 42;
        if (range.includes(q)) score += 32;
        for (const token of tokens) {
          if (title.includes(token)) score += 18;
          if (range.includes(token)) score += 12;
          if (body.includes(token)) score += 3;
        }
        if (score === 0) return { page, score: 0 };
        if (page.type === "ayah") score += 8;
        if (page.type === "tefsir-text") score += 5;
        return { page, score };
      })
      .filter(({ score }) => score > 2)
      .sort((a, b) => b.score - a.score || a.page.title.localeCompare(b.page.title, "tr"));

    const selected = [];
    const selectedPaths = new Set();
    const perSurah = new Map();
    for (const result of ranked) {
      const group = result.page.data.surah_key || "other";
      if ((perSurah.get(group) || 0) >= 3) continue;
      selected.push(result);
      selectedPaths.add(result.page.relative);
      perSurah.set(group, (perSurah.get(group) || 0) + 1);
      if (selected.length === limit) break;
    }
    for (const result of ranked) {
      if (selected.length === limit) break;
      if (selectedPaths.has(result.page.relative)) continue;
      selected.push(result);
    }

    return selected
      .map(({ page }) => ({
        title: page.title,
        type: page.type,
        typeLabel: pageTypeLabel(page.type),
        range: formatRange(page),
        excerpt: page.excerpt,
        href: publicPath(hrefFor(page)),
      }));
  }

  return { pages, lookup, ayahs, surahs, articles, transcripts, textArticles, search };
}

const store = loadContent();

function surahLinks(className = "") {
  return Object.values(SURAHS)
    .map((surah) => `<a class="${className}" href="/sure/${surah.key}">${surah.name}</a>`)
    .join("");
}

function hrefFor(page) {
  if (!page) return "#";
  if (page.relative === "Home") return "/";
  if (page.type === "surah") return `/sure/${surahFor(page).key}`;
  if (page.relative === "Tefsir Metinleri Indeksi") return "/metinler";
  if (page.type === "ayah") return `/sure/${surahFor(page).key}/ayet/${Number(page.data.ayah)}`;
  if (page.type === "tefsir-text") return `/metin/${Number(page.data.row_id)}`;
  if (page.type === "raw-transcript") return `/transkript/${Number(page.data.row_id)}`;
  return `/wiki/${encodeURIComponent(page.relative)}`;
}

function wikiLinks(text, seen = new Set()) {
  return text.replace(/!??\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]/g, (_, target, label) => {
    const page = store.lookup.get(target.trim().toLowerCase());
    const shown = (label || target).trim();
    if (!page) return `<span class="broken" title="Çözümlenemeyen bağlantı">${escapeHtml(shown)}</span>`;
    return `[${shown}](${hrefFor(page)})`;
  });
}

function youtubeSource(page) {
  const match = page?.content?.match(/^- Video:\s*(https?:\/\/\S+)\s*$/m);
  if (!match) return null;
  try {
    const url = new URL(match[1]);
    const host = url.hostname.replace(/^www\./, "");
    let id = "";
    if (host === "youtu.be") id = url.pathname.split("/").filter(Boolean)[0] || "";
    if (host === "youtube.com" || host === "m.youtube.com") {
      id = url.searchParams.get("v") || url.pathname.match(/^\/(?:embed|shorts)\/([^/]+)/)?.[1] || "";
    }
    if (!/^[A-Za-z0-9_-]{6,}$/.test(id)) return null;
    return { id, url: match[1] };
  } catch {
    return null;
  }
}

function embeddedArticleContent(page) {
  const source = youtubeSource(page);
  const replacement = source
    ? `<figure class="video-embed"><div><iframe src="https://www.youtube-nocookie.com/embed/${source.id}" title="${escapeHtml(page.title)} videosu" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div><figcaption><a href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">YouTube'da aç <span aria-hidden="true">↗</span></a></figcaption></figure>`
    : `<aside class="video-embed video-embed--missing"><strong>Video bağlantısı mevcut değil</strong><p>Bu eski kaynak için doğrulanmış bir YouTube adresi kayıtlı değil. Yazılı metin ve ham transkript arşivde korunmaktadır.</p></aside>`;
  return stripTitle(page.content).replace(/^## Kaynak bilgisi\s*\n[\s\S]*?^---\s*$/m, `${replacement}\n\n`);
}

function renderMarkdown(text, seen = new Set()) {
  const expanded = text.replace(/!\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]/g, (_, target) => {
    const page = store.lookup.get(target.trim().toLowerCase());
    if (!page) return `<span class="broken">${escapeHtml(target)}</span>`;
    if (seen.has(page.relative)) return `<p class="muted">Döngüsel gömme engellendi: ${escapeHtml(page.title)}</p>`;
    const nextSeen = new Set(seen);
    nextSeen.add(page.relative);
    const content = embeddedArticleContent(page);
    const range = formatRange(page);
    return `
<section class="source-card" data-source-id="${escapeHtml(page.data.row_id || "")}">
  <div class="source-card__topline">
    <div>
      <span class="eyebrow">${escapeHtml(range || pageTypeLabel(page.type))}</span>
      <h2>${escapeHtml(page.title)}</h2>
    </div>
    <a class="quiet-link" href="${hrefFor(page)}">Kaynak metni aç <span aria-hidden="true">↗</span></a>
  </div>
  <div class="source-card__meta"><span>${page.readingMinutes} dk okuma</span><span>Hafif editörlü transkript</span></div>
  <div class="source-card__body">${renderMarkdown(content, nextSeen)}</div>
</section>
`;
  });
  const withCallouts = expanded.replace(/^> \[!(info|warning)\]\s*(.*)\n((?:^>.*(?:\n|$))*)/gm, (_match, kind, title, quotedBody) => {
    const calloutBody = quotedBody.replace(/^>\s?/gm, "").trim();
    return `\n<aside class="callout callout--${kind}"><span class="callout__mark">${kind === "warning" ? "!" : "i"}</span><div><strong>${escapeHtml(title)}</strong>${md.render(wikiLinks(calloutBody, seen))}</div></aside>\n`;
  });
  return md.render(wikiLinks(withCallouts, seen));
}

function tocFor(page) {
  const items = [];
  for (const match of page.content.matchAll(/^(#{2,3})\s+(.+)$/gm)) {
    const title = stripMarkdown(match[2]);
    if (/Kaynak bilgisi|Editoryal kayıt/.test(title) || title === page.title) continue;
    items.push({ level: match[1].length, title, id: slugify(title) });
  }
  return items.slice(0, 14);
}

function icon(name) {
  const paths = {
    menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.66 6.34l1.41-1.41"/>',
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    book: '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H11v16H6.5A2.5 2.5 0 0 0 4 21.5zM20 5.5A2.5 2.5 0 0 0 17.5 3H13v16h4.5a2.5 2.5 0 0 1 2.5 2.5z"/>',
    copy: '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M15 9V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h3"/>',
    close: '<path d="m6 6 12 12M18 6 6 18"/>',
  };
  return `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${paths[name] || ""}</svg>`;
}

function brandLogo(alt = "") {
  return `<img class="brand-mark" src="/assets/channel-logo.jpg" width="40" height="40" alt="${escapeHtml(alt)}">`;
}

function ayahRanges(surah, currentAyah = 0) {
  const ranges = [];
  for (let start = 1; start <= surah.ayahCount; start += 25) ranges.push([start, Math.min(start + 24, surah.ayahCount)]);
  return ranges.map(([start, end]) => {
    const open = currentAyah >= start && currentAyah <= end;
    const grid = Array.from({ length: end - start + 1 }, (_, index) => start + index)
      .map((ayah) => `<a class="ayah-dot ${ayah === currentAyah ? "is-current" : ""}" href="/sure/${surah.key}/ayet/${ayah}" aria-label="${surah.name} ${ayah}">${ayah}</a>`)
      .join("");
    return `<details class="range-group" ${open ? "open" : ""}><summary>${start}–${end}<span>${open ? "Şu an" : ""}</span></summary><div class="mini-ayah-grid">${grid}</div></details>`;
  }).join("");
}

function sidebar(currentPage) {
  const currentAyah = Number(currentPage?.data?.ayah || currentPage?.data?.ayah_start || 0);
  const currentSurah = surahFor(currentPage);
  const showAyahRanges = Boolean(currentPage?.data?.surah_key) && ["ayah", "surah", "tefsir-text", "raw-transcript"].includes(currentPage?.type);
  const collectionLinks = Object.values(SURAHS).map((surah) => `<a class="sidebar-link ${currentSurah.key === surah.key && ["ayah", "surah"].includes(currentPage?.type) ? "is-active" : ""}" href="/sure/${surah.key}"><span>${surah.name}</span><small>${surah.ayahCount} ayet</small></a>`).join("");
  return `
    <div class="sidebar__inner">
      <div class="sidebar__section">
        <span class="sidebar__label">Kütüphane</span>
        <a class="sidebar-link ${currentPage?.relative === "Home" ? "is-active" : ""}" href="/"><span>Genel bakış</span><small>Başlangıç</small></a>
        ${collectionLinks}
        <a class="sidebar-link ${currentPage?.type === "methodology" ? "is-active" : ""}" href="/wiki/Metodoloji"><span>Metodoloji</span><small>Nasıl hazırlandı?</small></a>
      </div>
      ${showAyahRanges ? `<div class="sidebar__section sidebar__ranges">
        <span class="sidebar__label">${currentSurah.name} · ayete git</span>
        ${ayahRanges(currentSurah, currentAyah)}
      </div>` : ""}
      <div class="sidebar__foot">
        <span class="status-dot"></span>
        <span>${store.textArticles.length} kaynak metin · ${store.ayahs.size} ayet</span>
      </div>
    </div>`;
}

function breadcrumbs(page) {
  if (!page || page.relative === "Home") return "";
  let parent = { label: "Kütüphane", href: "/" };
  if (page.type === "ayah") parent = { label: surahFor(page).name, href: `/sure/${surahFor(page).key}` };
  if (page.type === "tefsir-text") parent = { label: "Kaynak Arşivi", href: "/metinler" };
  if (page.type === "raw-transcript") parent = { label: "Kaynak arşivi", href: `/metin/${Number(page.data.row_id)}` };
  return `<nav class="breadcrumbs" aria-label="Sayfa yolu"><a href="/">Ana sayfa</a><span>/</span><a href="${parent.href}">${parent.label}</a><span>/</span><span>${escapeHtml(page.title)}</span></nav>`;
}

function ayahChips(page) {
  const start = Number(page.data.ayah_start || page.data.ayah || 0);
  const end = Number(page.data.ayah_end || start);
  if (!start) return "";
  return Array.from({ length: end - start + 1 }, (_, index) => start + index)
    .map((ayah) => `<a href="/sure/${surahFor(page).key}/ayet/${ayah}" class="ayah-chip ${Number(page.data.ayah) === ayah ? "is-current" : ""}">${ayah}</a>`)
    .join("");
}

function rightRail(page) {
  if (!page) return "";
  const toc = tocFor(page);
  const start = Number(page.data.ayah_start || page.data.ayah || 0);
  const end = Number(page.data.ayah_end || start);
  const rowId = Number(page.data.row_id || 0);
  const raw = store.transcripts.get(rowId);
  let primary = "";
  if (page.type === "ayah") {
    const ayah = Number(page.data.ayah);
    const surah = surahFor(page);
    primary = `<div class="rail-card rail-nav"><span class="rail-label">Ayet navigasyonu</span><div class="rail-nav__buttons">${ayah > 1 ? `<a href="/sure/${surah.key}/ayet/${ayah - 1}">← ${ayah - 1}</a>` : "<span></span>"}${ayah < surah.ayahCount ? `<a href="/sure/${surah.key}/ayet/${ayah + 1}">${ayah + 1} →</a>` : ""}</div></div>`;
  } else if (page.type === "tefsir-text") {
    primary = `<div class="rail-card"><span class="rail-label">Kapsanan ayetler</span><div class="ayah-chips">${ayahChips(page)}</div>${raw ? `<a class="rail-action" href="${hrefFor(raw)}">Ham transkripti gör ${icon("arrow")}</a>` : ""}</div>`;
  }
  const tocHtml = toc.length ? `<div class="rail-card toc"><span class="rail-label">Bu sayfada</span>${toc.map((item) => `<a class="toc-${item.level}" href="#${item.id}">${escapeHtml(item.title)}</a>`).join("")}</div>` : "";
  return `${primary}${tocHtml}<div class="rail-card rail-note"><span class="rail-label">Editoryal yaklaşım</span><p>Metin, konuşma dilinden yazı diline çok hafif müdahaleyle geçirilmiştir.</p><a href="/wiki/Metodoloji">Yöntemi incele</a></div>`;
}

function pageHero(page) {
  if (page.type === "ayah") {
    const ayah = Number(page.data.ayah);
    const surah = surahFor(page);
    return `<header class="page-hero ayah-hero"><div class="ayah-number">${ayah}</div><div><span class="eyebrow">${surah.name} sûresi · ${surah.number}. sûre</span><h1>${surah.name} ${ayah}</h1><p>Bu ayeti kapsayan en özgül video anlatımlarının yazılı metni.</p></div></header>`;
  }
  if (page.type === "tefsir-text") {
    return `<header class="page-hero text-hero"><span class="eyebrow">${escapeHtml(formatRange(page))} · Yazılı tefsir</span><h1>${escapeHtml(page.title)}</h1><div class="hero-meta"><span>${page.readingMinutes} dakika okuma</span><span>%${Math.round(Number(page.data.retention_ratio || 0) * 100)} transkript koruması</span><button class="copy-button" type="button" data-copy-link>${icon("copy")} Bağlantıyı kopyala</button></div><div class="ayah-chips hero-chips">${ayahChips(page)}</div></header>`;
  }
  if (page.type === "raw-transcript") {
    return `<header class="page-hero raw-hero"><span class="eyebrow">Kaynak arşivi · Değiştirilmemiş metin</span><h1>${escapeHtml(page.title)}</h1><p>Bu sayfa yerel kaynak tablodaki transkripti aynen korur.</p></header>`;
  }
  return `<header class="page-hero"><span class="eyebrow">${escapeHtml(pageTypeLabel(page.type))}</span><h1>${escapeHtml(page.title)}</h1></header>`;
}

function stripTitle(content) {
  return content.replace(/^[ \t\r\n]*#\s+[^\n]+\n+/, "");
}

function renderContentPage(page) {
  let content = stripTitle(page.content);
  if (page.type === "ayah") content = content.replace(/^##\s+(?:Âl-i İmrân|Nisâ|Mâide|A[‘']râf|En[‘']âm)\s+\d+(?:–\d+)?\s*$/gm, "");
  const body = renderMarkdown(content, new Set([page.relative]));
  const articleClass = page.type === "raw-transcript" ? "prose prose--raw" : "prose";
  return `${pageHero(page)}<article class="${articleClass}">${body}</article>`;
}

function fullAyahGrid(surah) {
  return Array.from({ length: surah.ayahCount }, (_, index) => index + 1)
    .map((ayah) => `<a href="/sure/${surah.key}/ayet/${ayah}" class="ayah-tile"><span>${ayah}</span><small>${surah.name}</small></a>`)
    .join("");
}

function ayahIndexBody(surah) {
  return `<header class="index-hero"><span class="eyebrow">${surah.number}. sûre · ${surah.ayahCount} ayet</span><h1>${surah.name}</h1><p>Bir ayet seçin. Sayfa, o ayeti kapsayan en özgül yazılı anlatımı otomatik olarak gösterir.</p></header><section class="index-surface"><div class="full-ayah-grid full-ayah-grid--large">${fullAyahGrid(surah)}</div></section>`;
}

function textIndexBody() {
  const cards = store.textArticles.map((page) => `<article class="text-card"><div class="text-card__range">${escapeHtml(formatRange(page))}</div><div><h2><a href="${hrefFor(page)}">${escapeHtml(page.title)}</a></h2><p>${escapeHtml(page.excerpt)}</p><div class="text-card__meta"><span>${page.readingMinutes} dk</span><span>%${Math.round(Number(page.data.retention_ratio || 0) * 100)} koruma</span></div></div><a class="text-card__arrow" href="${hrefFor(page)}" aria-label="Metni aç">${icon("arrow")}</a></article>`).join("");
  return `<header class="index-hero"><span class="eyebrow">Provenans ve kaynak kontrolü</span><h1>Kaynak Arşivi</h1><p>${store.textArticles.length} video anlatımının, ayet sayfalarında kullanılan kaynağa bağlı tam metinleri.</p></header><div class="filter-bar"><a class="filter-chip is-active" href="/metinler">Tümü <span>${store.textArticles.length}</span></a>${surahLinks("filter-chip")}<button class="filter-chip" type="button" data-open-search>Arşivde ara</button></div><section class="text-list">${cards}</section>`;
}

function navigation(currentPage) {
  return `<header class="site-header"><div class="header-inner"><button class="icon-button menu-button" type="button" data-toggle-sidebar aria-label="Menüyü aç">${icon("menu")}</button><a class="site-brand" href="/">${brandLogo()}<span><strong>Yazılı Tefsir</strong><small>Kaynak Kütüphanesi</small></span></a><nav class="desktop-nav" aria-label="Ana navigasyon"><a href="/#sureler">Sûreler</a><a href="/wiki/Metodoloji">Metodoloji</a></nav><div class="header-actions"><button class="search-trigger" type="button" data-open-search>${icon("search")}<span>Ara</span><kbd>⌘ K</kbd></button><button class="icon-button" type="button" data-theme-toggle aria-label="Temayı değiştir">${icon("sun")}</button></div></div></header>`;
}

function searchDialog() {
  return `<div class="search-modal" data-search-modal aria-hidden="true"><button class="search-backdrop" type="button" data-close-search aria-label="Aramayı kapat"></button><section class="search-panel" role="dialog" aria-modal="true" aria-label="Kütüphanede ara"><div class="search-input-wrap">${icon("search")}<input type="search" data-search-input placeholder="Ayet, konu veya ifade ara…" autocomplete="off"><button class="icon-button" type="button" data-close-search aria-label="Kapat">${icon("close")}</button></div><div class="search-hint"><span>Örnek: “tevhid”, “adalet”, “Nisâ 168”</span><span><kbd>ESC</kbd> kapat</span></div><div class="search-results" data-search-results><div class="search-empty">${brandLogo("180 Saniyede Tefsir")}<p>${store.textArticles.length} yazılı metin ve ${store.ayahs.size} ayet içinde arayın.</p></div></div></section></div>`;
}

function footer() {
  return `<footer class="site-footer"><div><a class="site-brand site-brand--footer" href="/">${brandLogo()}<span><strong>Yazılı Tefsir</strong><small>Kaynak Kütüphanesi</small></span></a><p>180 Saniyede Tefsir video anlatımlarının kaynağa sadık yazılı edisyonu.</p></div><div class="footer-links">${surahLinks()}<a href="/wiki/Metodoloji">Metodoloji</a><a href="https://www.youtube.com/@180saniyedetefsir" target="_blank" rel="noopener noreferrer">YouTube ↗</a></div></footer>`;
}

function shell({ req, title, description = DEFAULT_DESCRIPTION, body, page = null, layout = "reader" }) {
  const origin = (process.env.SITE_URL || `${req.protocol}://${req.get("host")}`).replace(/\/$/, "");
  const canonical = `${origin}${publicPath(req.path)}`;
  const socialImage = `${origin}${publicPath("/assets/og-cover.png")}`;
  const fullTitle = title === SITE_NAME ? title : `${title} · ${SITE_NAME}`;
  const currentAyah = Number(page?.data?.ayah || page?.data?.ayah_start || 0);
  const currentSurah = surahFor(page);
  const main = layout === "home"
    ? `<main class="home-main">${body}</main>`
    : `<div class="reader-shell"><aside class="sidebar" data-sidebar>${sidebar(page)}</aside><main class="reader-main">${breadcrumbs(page)}<div class="content-surface">${body}</div></main><aside class="right-rail">${rightRail(page)}</aside></div>`;
  const jsonLd = page?.type === "tefsir-text" ? `<script type="application/ld+json">${JSON.stringify({ "@context": "https://schema.org", "@type": "Article", headline: page.title, description, isPartOf: { "@type": "CreativeWorkSeries", name: SITE_NAME }, mainEntityOfPage: canonical })}</script>` : "";
  const html = `<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#10261f"><title>${escapeHtml(fullTitle)}</title><meta name="description" content="${escapeHtml(description)}"><link rel="canonical" href="${escapeHtml(canonical)}"><meta property="og:type" content="article"><meta property="og:title" content="${escapeHtml(fullTitle)}"><meta property="og:description" content="${escapeHtml(description)}"><meta property="og:url" content="${escapeHtml(canonical)}"><meta property="og:site_name" content="${SITE_NAME}"><meta property="og:image" content="${escapeHtml(socialImage)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Yazılı Tefsir Kütüphanesi"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="${escapeHtml(socialImage)}"><link rel="icon" href="/assets/channel-logo.jpg" type="image/jpeg"><link rel="apple-touch-icon" href="/assets/channel-logo.jpg"><link rel="manifest" href="/manifest.webmanifest"><link rel="stylesheet" href="/assets/style.css">${jsonLd}<script>try{const t=localStorage.getItem('araf-theme');if(t)document.documentElement.dataset.theme=t}catch(e){}</script></head><body data-base-path="${escapeHtml(BASE_PATH)}" data-page-title="${escapeHtml(page?.title || title)}" data-page-url="${escapeHtml(publicPath(req.path))}" data-page-type="${escapeHtml(page?.type || layout)}" data-surah="${currentSurah.key}" data-surah-name="${currentSurah.name}" data-ayah="${currentAyah}"><div class="reading-progress" data-reading-progress></div>${navigation(page)}${main}${footer()}${searchDialog()}<div class="toast" data-toast role="status"></div><script src="/assets/app.js" defer></script></body></html>`;
  return prefixInternalUrls(html);
}

function servePage(req, res, page) {
  if (!page) return res.status(404).send(notFound(req));
  const description = page.type === "ayah" ? `${surahFor(page).name} suresi ${page.data.ayah}. ayeti kapsayan kaynak video anlatımlarının yazılı metni.` : page.excerpt || DEFAULT_DESCRIPTION;
  res.send(shell({ req, title: page.title, description, body: renderContentPage(page), page }));
}

function notFound(req) {
  const body = `<section class="not-found">${brandLogo("180 Saniyede Tefsir")}<span class="eyebrow">404</span><h1>Bu sayfa bulunamadı.</h1><p>Aradığınız metin taşınmış veya adres yanlış yazılmış olabilir.</p><div><a class="button button--primary" href="/">Ana sayfaya dön</a><button class="button button--ghost" data-open-search>Arama yap</button></div></section>`;
  return shell({ req, title: "Sayfa bulunamadı", body, layout: "home" });
}

app.get("/", (req, res) => {
  const page = store.lookup.get("home");
  res.send(shell({ req, title: SITE_NAME, body: renderContentPage(page), page }));
});
app.get("/sure/:surah", (req, res) => {
  const surah = SURAHS[String(req.params.surah).toLowerCase()];
  if (!surah) return res.status(404).send(notFound(req));
  res.send(shell({ req, title: surah.name, body: ayahIndexBody(surah), page: store.surahs.get(surah.key) }));
});
app.get("/metinler", (req, res) => res.send(shell({ req, title: "Kaynak Arşivi", body: textIndexBody(), page: store.lookup.get("tefsir metinleri indeksi") })));
app.get("/sure/:surah/ayet/:number", (req, res) => servePage(req, res, store.ayahs.get(`${String(req.params.surah).toLowerCase()}:${Number(req.params.number)}`)));
app.get("/ayetler", (_req, res) => res.redirect(301, publicPath("/sure/araf")));
app.get("/ayet/:number", (req, res) => res.redirect(301, publicPath(`/sure/araf/ayet/${Number(req.params.number)}`)));
app.get("/metin/:id", (req, res) => servePage(req, res, store.articles.get(Number(req.params.id))));
app.get("/transkript/:id", (req, res) => servePage(req, res, store.transcripts.get(Number(req.params.id))));
app.get("/wiki/:note", (req, res) => {
  const target = decodeURIComponent(req.params.note).toLowerCase();
  servePage(req, res, store.lookup.get(target));
});

app.get("/api/search", (req, res) => {
  res.set("Cache-Control", "public, max-age=60");
  res.json(store.search(String(req.query.q || "")));
});

app.get("/manifest.webmanifest", (_req, res) => res.type("application/manifest+json").send(JSON.stringify({ name: SITE_NAME, short_name: "Yazılı Tefsir", start_url: publicPath("/"), display: "standalone", background_color: "#f6f2e8", theme_color: "#12352b", icons: [{ src: publicPath("/assets/channel-logo.jpg"), sizes: "256x256", type: "image/jpeg", purpose: "any" }] })));
app.get("/robots.txt", (req, res) => {
  const origin = (process.env.SITE_URL || `${req.protocol}://${req.get("host")}`).replace(/\/$/, "");
  res.type("text").send(`User-agent: *\nAllow: ${publicPath("/")}\nSitemap: ${origin}${publicPath("/sitemap.xml")}\n`);
});
app.get("/sitemap.xml", (req, res) => {
  const origin = (process.env.SITE_URL || `${req.protocol}://${req.get("host")}`).replace(/\/$/, "");
  const urls = ["/", ...Object.values(SURAHS).map((surah) => `/sure/${surah.key}`), "/metinler", ...[...store.ayahs.values()].map(hrefFor), ...store.textArticles.map(hrefFor)];
  res.type("application/xml").send(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls.map((url) => `<url><loc>${escapeHtml(origin + publicPath(url))}</loc></url>`).join("")}</urlset>`);
});
app.get("/healthz", (_req, res) => res.json({ ok: true, pages: store.pages.length, surahs: store.surahs.size, ayahs: store.ayahs.size, articles: store.textArticles.length }));
app.use((req, res) => res.status(404).send(notFound(req)));

app.listen(PORT, HOST, () => console.log(`${SITE_NAME}: http://${HOST}:${PORT}`));
