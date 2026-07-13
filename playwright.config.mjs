import { defineConfig, devices } from "@playwright/test";

const baseURL = process.env.TEST_BASE_URL || "http://127.0.0.1:4173";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  reporter: "line",
  webServer: {
    command: "npm start",
    url: new URL("/healthz", baseURL).href,
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
  use: {
    baseURL,
    trace: "retain-on-failure",
  },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"] } },
    { name: "mobile", use: { ...devices["iPhone 13"], browserName: "chromium" } },
  ],
});
