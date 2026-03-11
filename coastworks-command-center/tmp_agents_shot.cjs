const { chromium } = require('playwright-core');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  await page.goto('http://localhost:4310', { waitUntil: 'networkidle' });
  await page.click('button[data-tab="agents"]');
  await page.waitForTimeout(700);
  await page.screenshot({ path: 'C:/Users/ryd/.openclaw/workspace/coastworks-command-center/agents-screenshot.png', fullPage: true });
  await browser.close();
})();