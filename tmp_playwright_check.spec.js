const { test, expect } = require('playwright/test');

test('capture authenticated home page', async({ page }) => {
  await page.goto('http://127.0.0.1:8000/login/');
  await page.fill('input[name="username"]', 'mik');
  await page.fill('input[name="password"]', 'Novator123!');
  await page.click('button[type="submit"]');
  await page.waitForURL('http://127.0.0.1:8000/');
  await expect(page).toHaveTitle(/Главная|Novator/i);
  await page.screenshot({ path: '/tmp/novator-home.png', fullPage: true });
});
