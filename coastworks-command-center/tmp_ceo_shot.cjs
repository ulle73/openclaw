const { chromium } = require('playwright-core');

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe' });
  const page = await browser.newPage({ viewport: { width: 1700, height: 1200 } });
  await page.goto('http://localhost:4310', { waitUntil: 'networkidle' });
  await page.click('button[data-tab="ceo"]');
  await page.waitForTimeout(1000);
  await page.screenshot({ path: 'C:/Users/ryd/.openclaw/workspace/coastworks-command-center/ceo-vy-snapshot.png', fullPage: true });
  await browser.close();
})();