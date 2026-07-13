import { expect, test } from "@playwright/test";

test("home is the wiki index and exposes the searchable library", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toContainText("Yazılı Tefsir Kütüphanesi");
  await expect(page.locator(".site-header .brand-mark")).toHaveAttribute("src", "/assets/channel-logo.jpg");
  await expect(page.locator(".home-hero, .surah-card")).toHaveCount(0);
  await expect(page.locator(".site-header a[href='/metinler'], [data-sidebar] a[href='/metinler'], .site-footer a[href='/metinler']")).toHaveCount(0);
  for (const href of ["ali-imran", "nisa", "maide", "enam", "araf"]) {
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
  await expect(page.locator(".text-card")).toHaveCount(331);
});

test("search returns only genuine matches across the five surahs", async ({ request }) => {
  const nisa = await request.get("/api/search?q=Nisâ%20168").then((response) => response.json());
  expect(nisa.some((result) => result.href === "/sure/nisa/ayet/168")).toBeTruthy();

  const maide = await request.get("/api/search?q=adalet").then((response) => response.json());
  expect(maide.some((result) => result.href.startsWith("/metin/") && result.range.startsWith("Mâide"))).toBeTruthy();

  const faith = await request.get("/api/search?q=iman").then((response) => response.json());
  for (const surah of ["Âl-i İmrân", "Nisâ", "Mâide", "En‘âm", "A‘râf"]) {
    expect(faith.some((result) => result.range.startsWith(surah))).toBeTruthy();
  }

  const impossible = await request.get("/api/search?q=zzzyokturzzz").then((response) => response.json());
  expect(impossible).toEqual([]);
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
