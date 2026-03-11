const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('C:/Users/ryd/AppData/Roaming/npm/node_modules/openclaw/node_modules/playwright-core');

(async () => {
  const outDir = path.resolve('C:/Users/ryd/.openclaw/workspace/tmp/command-center-shots');
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true,
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 960 } });
  const page = await context.newPage();
  await page.goto('http://localhost:4310', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(1200);

  const categories = [
    ['oversikt', 'Översikt'],
    ['agenter', 'Agenter'],
    ['kanban', 'Kanban'],
    ['youtube-ingest', 'YouTube Ingest'],
    ['kunskapsbank', 'Kunskapsbank'],
    ['daglig-historik', 'Daglig historik'],
    ['workspace-mirror', 'Workspace Mirror'],
  ];

  const outputs = [];
  for (const [slug, label] of categories) {
    const item = page.getByRole('button', { name: label, exact: true });
    const count = await item.count();
    if (count > 0) {
      await item.first().click();
      await page.waitForTimeout(600);
    }
    const outPath = path.join(outDir, `${slug}.png`);
    await page.screenshot({ path: outPath, fullPage: true });
    outputs.push(outPath);
  }

  await browser.close();
  console.log(JSON.stringify(outputs, null, 2));
})().catch((err) => {
  console.error(err);
  process.exit(1);
});