#!/usr/bin/env node

const path = require("node:path");
const fs = require("node:fs");

const PLAYWRIGHT_CORE = "C:/Users/ryd/AppData/Roaming/npm/node_modules/openclaw/node_modules/playwright-core";
const { chromium } = require(PLAYWRIGHT_CORE);

const DEFAULT_TIMEOUT_MS = 30000;
const DEFAULT_WAIT_MS = 1200;
const DEFAULT_TEXT_LIMIT = 8000;

function findChromeExecutable() {
  const candidates = [
    process.env.CHROME_PATH,
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  ].filter(Boolean);

  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }
  throw new Error("No supported Chrome/Edge executable found. Set CHROME_PATH.");
}

function parseArgs(argv) {
  const [command, ...rest] = argv;
  const options = {
    command: command || "",
    url: "",
    selector: "body",
    limit: DEFAULT_TEXT_LIMIT,
    timeout: DEFAULT_TIMEOUT_MS,
    waitMs: DEFAULT_WAIT_MS,
    json: false,
    output: "",
  };

  const positionals = [];
  for (let index = 0; index < rest.length; index += 1) {
    const token = rest[index];
    if (token === "--json") {
      options.json = true;
      continue;
    }
    if (token === "--selector") {
      options.selector = rest[index + 1] || options.selector;
      index += 1;
      continue;
    }
    if (token === "--limit") {
      options.limit = Number(rest[index + 1] || options.limit);
      index += 1;
      continue;
    }
    if (token === "--timeout") {
      options.timeout = Number(rest[index + 1] || options.timeout);
      index += 1;
      continue;
    }
    if (token === "--wait-ms") {
      options.waitMs = Number(rest[index + 1] || options.waitMs);
      index += 1;
      continue;
    }
    if (token === "--output") {
      options.output = rest[index + 1] || "";
      index += 1;
      continue;
    }
    positionals.push(token);
  }

  options.url = positionals[0] || "";
  if (options.command === "screenshot") {
    options.output = options.output || positionals[1] || "";
  }
  return options;
}

function usage() {
  const lines = [
    "Usage:",
    "  node scripts/browser_host.js title <url> [--json]",
    "  node scripts/browser_host.js extract <url> [--selector body] [--limit 8000] [--wait-ms 1200] [--json]",
    "  node scripts/browser_host.js links <url> [--limit 20] [--wait-ms 1200] [--json]",
    "  node scripts/browser_host.js screenshot <url> <output-path> [--wait-ms 1200] [--json]",
  ];
  console.error(lines.join("\n"));
}

async function withBrowser(fn, timeout) {
  const executablePath = findChromeExecutable();
  let lastError = null;

  for (let attempt = 1; attempt <= 2; attempt += 1) {
    let browser;
    try {
      browser = await chromium.launch({
        executablePath,
        headless: true,
        timeout,
        args: [
          "--disable-dev-shm-usage",
          "--disable-background-networking",
          "--disable-background-timer-throttling",
          "--disable-renderer-backgrounding",
          "--no-first-run",
          "--no-default-browser-check",
        ],
      });
      const result = await fn(browser);
      await browser.close();
      return result;
    } catch (error) {
      lastError = error;
      if (browser) {
        try {
          await browser.close();
        } catch {}
      }
      if (attempt < 2) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
      }
    }
  }

  throw lastError || new Error("Unknown browser failure");
}

async function loadPage(browser, options) {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 960 },
    userAgent:
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
  });
  const page = await context.newPage();
  await page.goto(options.url, {
    waitUntil: "domcontentloaded",
    timeout: options.timeout,
  });
  if (options.waitMs > 0) {
    await page.waitForTimeout(options.waitMs);
  }
  return { context, page };
}

function normalizeText(text, limit) {
  const normalized = String(text || "").replace(/\s+/g, " ").trim();
  if (!limit || normalized.length <= limit) {
    return normalized;
  }
  return normalized.slice(0, limit).trim();
}

async function commandTitle(options) {
  return withBrowser(async (browser) => {
    const { context, page } = await loadPage(browser, options);
    const payload = {
      url: page.url(),
      title: await page.title(),
    };
    await context.close();
    return payload;
  }, options.timeout);
}

async function commandExtract(options) {
  return withBrowser(async (browser) => {
    const { context, page } = await loadPage(browser, options);
    const text = await page.locator(options.selector).innerText({ timeout: options.timeout });
    const payload = {
      url: page.url(),
      title: await page.title(),
      text: normalizeText(text, options.limit),
    };
    await context.close();
    return payload;
  }, options.timeout);
}

async function commandLinks(options) {
  return withBrowser(async (browser) => {
    const { context, page } = await loadPage(browser, options);
    const rawLinks = await page.$$eval("a[href]", (anchors) =>
      anchors.map((anchor) => ({
        text: (anchor.textContent || "").replace(/\s+/g, " ").trim(),
        href: anchor.href || "",
      })),
    );
    const links = [];
    const seen = new Set();
    for (const link of rawLinks) {
      const key = `${link.text}@@${link.href}`;
      if (!link.href || seen.has(key)) {
        continue;
      }
      seen.add(key);
      links.push(link);
      if (links.length >= options.limit) {
        break;
      }
    }
    const payload = {
      url: page.url(),
      title: await page.title(),
      links,
    };
    await context.close();
    return payload;
  }, options.timeout);
}

async function commandScreenshot(options) {
  if (!options.output) {
    throw new Error("screenshot requires an output path");
  }
  return withBrowser(async (browser) => {
    const { context, page } = await loadPage(browser, options);
    const outputPath = path.resolve(options.output);
    await page.screenshot({ path: outputPath, fullPage: true });
    const payload = {
      url: page.url(),
      title: await page.title(),
      output: outputPath,
    };
    await context.close();
    return payload;
  }, options.timeout);
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (!options.command || !options.url) {
    usage();
    process.exit(1);
  }

  let payload;
  if (options.command === "title") {
    payload = await commandTitle(options);
  } else if (options.command === "extract") {
    payload = await commandExtract(options);
  } else if (options.command === "links") {
    payload = await commandLinks(options);
  } else if (options.command === "screenshot") {
    payload = await commandScreenshot(options);
  } else {
    usage();
    process.exit(1);
  }

  if (options.json) {
    console.log(JSON.stringify(payload, null, 2));
    return;
  }

  if (options.command === "title") {
    console.log(payload.title);
    return;
  }

  if (options.command === "extract") {
    console.log(`# ${payload.title}\n${payload.url}\n\n${payload.text}`);
    return;
  }

  if (options.command === "links") {
    console.log(`# ${payload.title}\n${payload.url}`);
    for (const link of payload.links) {
      console.log(`- ${link.text || "(no text)"} :: ${link.href}`);
    }
    return;
  }

  if (options.command === "screenshot") {
    console.log(payload.output);
  }
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
