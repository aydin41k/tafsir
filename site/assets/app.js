const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

const sidebar = $("[data-sidebar]");
const modal = $("[data-search-modal]");
const searchInput = $("[data-search-input]");
const searchResults = $("[data-search-results]");
const basePath = document.body.dataset.basePath || "";
const toast = $("[data-toast]");
let previousFocus = null;

function setSidebar(open) {
  document.body.classList.toggle("sidebar-open", open);
  sidebar?.classList.toggle("is-open", open);
  $("[data-toggle-sidebar]")?.setAttribute("aria-expanded", String(open));
}

function setSearch(open) {
  if (!modal) return;
  if (open) previousFocus = document.activeElement;
  modal.classList.toggle("is-open", open);
  modal.setAttribute("aria-hidden", String(!open));
  document.body.classList.toggle("modal-open", open);
  if (open) setTimeout(() => searchInput?.focus(), 40);
  else if (previousFocus instanceof HTMLElement) previousFocus.focus();
}

$$('[data-toggle-sidebar]').forEach((button) => button.addEventListener("click", () => setSidebar(!document.body.classList.contains("sidebar-open"))));
$$('[data-open-search]').forEach((button) => button.addEventListener("click", () => setSearch(true)));
$$('[data-close-search]').forEach((button) => button.addEventListener("click", () => setSearch(false)));
$$('.sidebar a').forEach((link) => link.addEventListener("click", () => setSidebar(false)));

document.addEventListener("pointerdown", (event) => {
  if (!document.body.classList.contains("sidebar-open") || !sidebar) return;
  const toggle = event.target.closest?.("[data-toggle-sidebar]");
  const box = sidebar.getBoundingClientRect();
  const hitScrim = event.target === sidebar && event.clientX > box.right;
  if ((!sidebar.contains(event.target) && !toggle) || hitScrim) setSidebar(false);
});

document.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    setSearch(true);
  } else if (event.key === "/" && !/input|textarea/i.test(document.activeElement?.tagName || "")) {
    event.preventDefault();
    setSearch(true);
  } else if (event.key === "Escape") {
    setSearch(false);
    setSidebar(false);
  } else if (modal?.classList.contains("is-open") && ["ArrowDown", "ArrowUp", "Enter"].includes(event.key)) {
    const links = $$(".search-result", searchResults);
    if (!links.length) return;
    const current = links.indexOf(document.activeElement);
    if (event.key === "Enter" && current >= 0) return;
    event.preventDefault();
    const next = event.key === "ArrowUp"
      ? (current <= 0 ? links.length - 1 : current - 1)
      : (current + 1) % links.length;
    links[next].focus();
  }
});

let searchTimer;
searchInput?.addEventListener("input", () => {
  clearTimeout(searchTimer);
  const query = searchInput.value.trim();
  if (query.length < 2) {
    searchResults.innerHTML = '<div class="search-empty"><span class="brand-mark">۞</span><p>En az iki karakter yazın.</p></div>';
    return;
  }
  searchResults.innerHTML = '<div class="search-loading"><span></span><span></span><span></span></div>';
  searchTimer = setTimeout(async () => {
    try {
      const results = await fetch(`${basePath}/api/search?q=${encodeURIComponent(query)}`).then((response) => response.json());
      if (!results.length) {
        searchResults.innerHTML = `<div class="search-empty"><p>“${escapeHtml(query)}” için sonuç bulunamadı.</p></div>`;
        return;
      }
      searchResults.innerHTML = results.map((result) => `
        <a class="search-result" href="${result.href}">
          <span class="search-result__icon">${result.type === "ayah" ? result.title.replace(/\D/g, "") : "↗"}</span>
          <span><small>${result.range || result.typeLabel}</small><strong>${escapeHtml(result.title)}</strong><p>${escapeHtml(result.excerpt)}</p></span>
          <em>${result.typeLabel}</em>
        </a>`).join("");
    } catch {
      searchResults.innerHTML = '<div class="search-empty"><p>Arama şu anda kullanılamıyor.</p></div>';
    }
  }, 160);
});

function escapeHtml(value = "") {
  const node = document.createElement("div");
  node.textContent = value;
  return node.innerHTML;
}

$$('[data-theme-toggle]').forEach((button) => button.addEventListener("click", () => {
  const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = next;
  localStorage.setItem("araf-theme", next);
}));

function showToast(message) {
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add("is-visible");
  setTimeout(() => toast.classList.remove("is-visible"), 1800);
}

$$('[data-copy-link]').forEach((button) => button.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(location.href);
    showToast("Bağlantı kopyalandı");
  } catch {
    showToast("Bağlantı: " + location.href);
  }
}));

const progress = $("[data-reading-progress]");
function updateProgress() {
  if (!progress) return;
  const max = document.documentElement.scrollHeight - innerHeight;
  progress.style.transform = `scaleX(${max > 0 ? Math.min(1, scrollY / max) : 0})`;
}
addEventListener("scroll", updateProgress, { passive: true });
updateProgress();

try {
  const type = document.body.dataset.pageType;
  const url = document.body.dataset.pageUrl;
  const resumable = ["ayah", "tefsir-text"].includes(type) && url;
  const saved = JSON.parse(localStorage.getItem("araf-last-read") || "null");
  const wantsResume = saved?.url === location.pathname && new URLSearchParams(location.search).has("resume");
  let saveTimer;
  const saveReadingState = () => {
    if (!resumable) return;
    const max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    localStorage.setItem("araf-last-read", JSON.stringify({
      title: document.body.dataset.pageTitle,
      url,
      type,
      ayah: document.body.dataset.ayah,
      surah: document.body.dataset.surah,
      surahName: document.body.dataset.surahName,
      progress: Math.min(1, scrollY / max),
      savedAt: Date.now(),
    }));
  };
  if (!wantsResume) saveReadingState();
  if (resumable) addEventListener("scroll", () => {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(saveReadingState, 180);
  }, { passive: true });
  const section = $("#continue-section");
  if (saved && section && saved.url !== location.pathname) {
    section.hidden = false;
    $("#continue-card").href = `${saved.url}?resume=1`;
    $("#continue-title").textContent = saved.title;
    $("#continue-kicker").textContent = saved.type === "ayah" ? `${saved.surahName || "Sûre"} ${saved.ayah}` : "Yazılı tefsir";
    $("#continue-time").textContent = saved.progress > 0.05 ? `%${Math.round(saved.progress * 100)} tamamlandı` : "Son okuduğunuz yer";
  }
  if (wantsResume && saved.progress > 0.02) {
    requestAnimationFrame(() => requestAnimationFrame(() => {
      const max = document.documentElement.scrollHeight - innerHeight;
      scrollTo({ top: max * saved.progress, behavior: "smooth" });
    }));
  }
} catch {}

const observer = new IntersectionObserver((entries) => {
  for (const entry of entries) if (entry.isIntersecting) entry.target.classList.add("is-visible");
}, { threshold: 0.08 });
$$('.principle-grid article, .text-card, .ayah-tile').forEach((element) => {
  element.classList.add("reveal");
  observer.observe(element);
});

const tocLinks = $$(".toc a");
if (tocLinks.length) {
  const headings = tocLinks.map((link) => $(link.getAttribute("href"))).filter(Boolean);
  const tocObserver = new IntersectionObserver((entries) => {
    const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
    if (!visible) return;
    tocLinks.forEach((link) => link.classList.toggle("is-active", link.getAttribute("href") === `#${visible.target.id}`));
  }, { rootMargin: "-15% 0px -72%", threshold: 0 });
  headings.forEach((heading) => tocObserver.observe(heading));
}
