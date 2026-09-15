import { expect, test } from "@playwright/test";

test("home is the wiki index and exposes the searchable library", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toContainText("Yazılı Tefsir Kütüphanesi");
  await expect(page.locator(".site-header .brand-mark")).toHaveAttribute("src", "/assets/channel-logo.jpg");
  await expect(page.locator(".home-hero, .surah-card")).toHaveCount(0);
  await expect(page.locator(".site-header a[href='/metinler'], [data-sidebar] a[href='/metinler'], .site-footer a[href='/metinler']")).toHaveCount(0);
  for (const href of ["ali-imran", "nisa", "maide", "enam", "araf", "enfal"]) {
    await expect(page.locator(`a[href='/sure/${href}']`).first()).toBeVisible();
  }

  await page.keyboard.press("ControlOrMeta+K");
  await expect(page.locator("[data-search-modal]")).toHaveClass(/is-open/);
  await page.locator("[data-search-input]").fill("zikir");
  await expect(page.locator(".search-result").first()).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(page.locator("[data-search-modal]")).not.toHaveClass(/is-open/);
});

test("ayah reader renders source-faithful articles without vault syntax", async ({ page }) => {
  await page.goto("/sure/araf/ayet/54");
  await expect(page.locator(".source-card")).toHaveCount(5);
  await expect(page.locator(".source-card").first()).toBeVisible();
  await expect(page.locator(".source-card iframe[src*='youtube-nocookie.com/embed/']")).toHaveCount(5);
  await expect(page.getByRole("heading", { name: "Kaynak bilgisi" })).toHaveCount(0);
  await expect(page.locator(".source-card .quiet-link").first()).toHaveAttribute("href", /\/metin\/\d+/);
  await expect(page.locator(".source-card .quiet-link").first()).toContainText("Kaynak metni aç");
  await expect(page.locator("body")).not.toContainText("[!info]");
  await expect(page.locator(".callout").first()).toContainText("Kaynak metin");

  await page.locator("[data-theme-toggle]").click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
});

test("source archive remains available as a secondary provenance view", async ({ page }) => {
  await page.goto("/metinler");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Kaynak Arşivi");
  await expect(page.locator(".text-card")).toHaveCount(393);
});

test("search returns only genuine matches across the six surahs", async ({ request }) => {
  const nisa = await request.get("/api/search?q=Nisâ%20168").then((response) => response.json());
  expect(nisa.some((result) => result.href === "/sure/nisa/ayet/168")).toBeTruthy();

  const maide = await request.get("/api/search?q=adalet").then((response) => response.json());
  expect(maide.some((result) => result.href.startsWith("/sure/maide/ayet/") && result.href.includes("#kaynak-") && result.range.startsWith("Mâide"))).toBeTruthy();
  expect(maide.some((result) => result.href.startsWith("/metin/"))).toBeFalsy();

  const faith = await request.get("/api/search?q=iman").then((response) => response.json());
  for (const surah of ["Âl-i İmrân", "Nisâ", "Mâide", "En‘âm", "A‘râf", "Enfâl"]) {
    expect(faith.some((result) => result.range.startsWith(surah))).toBeTruthy();
  }

  const impossible = await request.get("/api/search?q=zzzyokturzzz").then((response) => response.json());
  expect(impossible).toEqual([]);
});

test("search opens full-text matches on the ayah page and highlights their source", async ({ page }) => {
  await page.goto("/");
  await page.keyboard.press("ControlOrMeta+K");
  await page.locator("[data-search-input]").fill("adalet");
  const sourceResult = page.locator(".search-result[href*='/sure/'][href*='#kaynak-']").first();
  await expect(sourceResult).toBeVisible();
  await sourceResult.click();

  await expect(page).toHaveURL(/\/sure\/[^/]+\/ayet\/\d+#kaynak-\d+$/);
  await expect(page.locator(".source-card:target")).toHaveCount(1);
  await expect(page.locator(".source-card:target")).toBeInViewport();
});

test("search links a ranged source only to an ayah where it is embedded", async ({ request }) => {
  const results = await request.get("/api/search?q=Enfal%202-3").then((response) => response.json());
  const source = results.find((result) => result.title === "Enfal 2-3");
  expect(source?.href).toBe("/sure/enfal/ayet/3#kaynak-377");
});

test("written prose spells out sentence-initial numbers", async ({ page }) => {
  await page.goto("/sure/nisa/ayet/8");
  await expect(page.locator(".source-card__body").first()).toContainText("Yedinci ayette dedik ki");
  await expect(page.locator(".source-card__body").first()).not.toContainText("7. ayette dedik ki");
});

test("article headings render without visible Markdown markers", async ({ page }) => {
  await page.goto("/sure/enam/ayet/35");
  await expect(page.getByRole("heading", { name: "En‘âm 35. ayetin meali ve cümle yapısı" })).toBeVisible();
  await expect(page.locator(".source-card__body").first()).not.toContainText("## En‘âm 35");
});

test("new surah collections expose covered and intentionally missing ayahs", async ({ page }) => {
  await page.goto("/sure/ali-imran/ayet/7");
  await expect(page.locator(".source-card").first()).toBeVisible();

  await page.goto("/sure/ali-imran/ayet/1");
  await expect(page.locator(".source-card")).toHaveCount(0);
  await expect(page.locator(".callout--warning")).toBeVisible();

  await page.goto("/sure/nisa/ayet/168");
  await expect(page.locator(".source-card").first()).toBeVisible();

  await page.goto("/sure/maide/ayet/6");
  await expect(page.locator(".source-card").first()).toBeVisible();

  await page.goto("/sure/enfal/ayet/75");
  await expect(page.locator(".source-card").first()).toBeVisible();

  await page.goto("/sure/enfal/ayet/1");
  await expect(page.locator(".source-card")).toHaveCount(3);
  await expect(page.locator(".source-card iframe[src*='youtube-nocookie.com/embed/hC9aWGqbGtI']")).toHaveCount(1);

  await page.goto("/sure/enfal/ayet/67");
  await expect(page.locator(".source-card")).toHaveCount(2);
});

test("the book index lists every chapter and marks the text as original", async ({ page }) => {
  await page.goto("/kitap/furkan-gunu");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Furkān Günü");
  await expect(page.locator(".index-hero .eyebrow")).toContainText("Telif kitap · 8 bölüm");
  await expect(page.locator(".text-card")).toHaveCount(8);
  await expect(page.locator(".text-card").first().locator("h2 a")).toHaveAttribute("href", "/kitap/furkan-gunu/bolum/1");
  await expect(page.locator(".filter-bar a[href='/kitap/furkan-gunu/dizin']")).toBeVisible();
  await expect(page.locator(".filter-bar a[href='/wiki/Metodoloji#telif-kitap']")).toBeVisible();
});

test("a chapter reads as clean prose and carries the original-text notice", async ({ page }) => {
  await page.goto("/kitap/furkan-gunu/bolum/1");
  await expect(page.locator(".chapter-hero .eyebrow")).toHaveText("Furkān Günü · 1. bölüm");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Yesrib'in Yemi");
  await expect(page.locator(".prose--book p").first()).toBeVisible();
  await expect(page.locator(".prose--book")).not.toContainText("[[");
  await expect(page.locator(".prose--book")).not.toContainText("--");
  await expect(page.locator(".prose--book .broken")).toHaveCount(0);
  await expect(page.locator("body")).toHaveAttribute("data-book", "Furkān Günü");
  await expect(page.locator("body")).toHaveAttribute("data-page-type", "book-chapter");
});

test("chapter navigation walks the book and ends on the appendix", async ({ page }) => {
  await page.goto("/kitap/furkan-gunu/bolum/1");
  await expect(page.locator(".chapter-nav__link--previous")).toHaveCount(0);
  await page.locator(".chapter-nav__link--next").click();
  await expect(page).toHaveURL(/\/kitap\/furkan-gunu\/bolum\/2$/);
  await page.locator(".chapter-nav__link--previous").click();
  await expect(page).toHaveURL(/\/kitap\/furkan-gunu\/bolum\/1$/);

  await page.goto("/kitap/furkan-gunu/bolum/8");
  await expect(page.locator(".chapter-nav__link--next")).toContainText("Enfâl Âyet Dizini");
  await page.locator(".chapter-nav__link--next").click();
  await expect(page).toHaveURL(/\/kitap\/furkan-gunu\/dizin$/);
});

test("the appendix ties the book back to the Enfâl ayah pages", async ({ page }) => {
  await page.goto("/kitap/furkan-gunu/dizin");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Enfâl Âyet Dizini");
  await expect(page.locator(".prose a[href='/sure/enfal/ayet/42']").first()).toBeVisible();
  await expect(page.locator(".prose a[href='/kitap/furkan-gunu/bolum/3']").first()).toBeVisible();
  await expect(page.locator(".prose .broken")).toHaveCount(0);
  await expect(page.locator(".callout--warning")).toContainText("Numarası verilmeyen âyet");
  await expect(page.locator(".breadcrumbs a[href='/kitap/furkan-gunu']")).toHaveCount(1);
});

test("the book is reachable from global navigation and search", async ({ page, request }) => {
  await page.goto("/");
  await expect(page.locator(".site-footer a[href='/kitap/furkan-gunu']")).toBeVisible();

  const results = await request.get("/api/search?q=Yelyel").then((response) => response.json());
  const chapter = results.find((result) => result.href === "/kitap/furkan-gunu/bolum/3");
  expect(chapter?.typeLabel).toBe("Kitap bölümü");

  const health = await request.get("/healthz").then((response) => response.json());
  expect(health.books).toBe(1);
  expect(health.chapters).toBe(8);
});

test("mobile navigation opens and leads to the ayah index", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "mobile", "mobile-only interaction");
  await page.goto("/sure/nisa/ayet/168");
  await page.locator("[data-toggle-sidebar]").click();
  await expect(page.locator("[data-sidebar]")).toHaveClass(/is-open/);
  await page.locator("[data-sidebar] a[href='/sure/nisa']").click();
  await expect(page).toHaveURL(/\/sure\/nisa$/);
  await expect(page.locator(".ayah-tile")).toHaveCount(176);
});
