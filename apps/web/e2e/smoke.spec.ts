import { test, expect } from "@playwright/test";
import fs from "fs";
import path from "path";

test.describe("Web Skeleton Smoke Test", () => {
  test("loads home page and displays healthy API status", async ({ page }, testInfo) => {
    await page.goto("/");

    const pageTitle = page.locator('[data-testid="page-title"]');
    await expect(pageTitle).toBeVisible({ timeout: 15000 });
    await expect(pageTitle).toHaveText("PACE AI Hub");

    const statusText = page.locator('[data-testid="api-status-text"]');
    await expect(statusText).toBeVisible();
    await expect(statusText).toContainText("Đang hoạt động (ok)");

    const iconOk = page.locator('[data-testid="icon-ok"]');
    await expect(iconOk).toBeVisible();

    // Capture screenshot as required by DoD
    const screenshotsDir = path.resolve(__dirname, "../screenshots");
    if (!fs.existsSync(screenshotsDir)) {
      fs.mkdirSync(screenshotsDir, { recursive: true });
    }
    const screenshotPath = path.join(screenshotsDir, `home-${testInfo.project.name}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: true });
  });
});
