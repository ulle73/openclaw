import { setTimeout as wait } from 'node:timers/promises';

const cities = [
  'Stockholm','Göteborg','Malmö','Uppsala','Västerås','Örebro','Linköping','Helsingborg','Jönköping','Norrköping',
  'Lund','Umeå','Gävle','Borås','Södertälje','Eskilstuna','Halmstad','Växjö','Karlstad','Sundsvall',
  'Östersund','Luleå','Kalmar','Skellefteå','Kristianstad','Falun','Trollhättan','Nyköping','Varberg','Visby'
];

const emailRegex = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
const badDomains = ['example.com','wixpress.com','sentry.io','loopia.com','loopia.se','loopia.no','loopia.rs'];
const badEmails = ['fornamn.efternamn@','firstname.lastname@','inside.sales.leads@'];

function extractDomain(url) {
  try { return new URL(url).hostname.replace(/^www\./,'').toLowerCase(); } catch { return ''; }
}

function looksBad(email) {
  const e = email.toLowerCase();
  if (badDomains.some(d => e.endsWith('@'+d) || e.includes(d))) return true;
  if (badEmails.some(x => e.includes(x))) return true;
  return false;
}

function scoreEmail(email, pageDomain) {
  const e = email.toLowerCase();
  let s = 0;
  if (e.startsWith('info@') || e.startsWith('kontakt@') || e.startsWith('hej@') || e.startsWith('mail@')) s += 5;
  if (pageDomain && e.endsWith('@'+pageDomain)) s += 8;
  if (e.includes('karriar') || e.includes('career')) s -= 5;
  if (e.includes('support')) s -= 4;
  return s;
}

async function search(city) {
  const q = encodeURIComponent(`redovisningsbyrå ${city} kontakt e-post`);
  const url = `https://www.bing.com/search?q=${q}`;
  const html = await (await fetch(url, { headers: { 'user-agent': 'Mozilla/5.0' } })).text();
  const links = [];
  const re = /<a href="(https?:\/\/[^"#]+)" h=/g;
  let m;
  while ((m = re.exec(html)) && links.length < 20) {
    const u = m[1].replaceAll('&amp;','&');
    if (u.includes('bing.com') || u.includes('microsoft.com')) continue;
    if (!links.includes(u)) links.push(u);
  }
  return links;
}

const picked = [];
const usedEmails = new Set();
const usedDomains = new Set();

for (const city of cities) {
  if (picked.length >= 30) break;
  let links = [];
  try { links = await search(city); } catch { continue; }

  for (const link of links) {
    if (picked.length >= 30) break;
    let html = '';
    try {
      html = await (await fetch(link, { headers: { 'user-agent': 'Mozilla/5.0' } })).text();
    } catch { continue; }

    const pageDomain = extractDomain(link);
    const emails = [...new Set((html.match(emailRegex) || []))]
      .filter(e => !looksBad(e));
    if (!emails.length) continue;

    const ranked = emails.sort((a,b)=>scoreEmail(b,pageDomain)-scoreEmail(a,pageDomain));
    const chosen = ranked[0].toLowerCase();
    const emailDomain = chosen.split('@')[1] || '';
    if (usedEmails.has(chosen)) continue;
    if (usedDomains.has(emailDomain)) continue;

    usedEmails.add(chosen);
    usedDomains.add(emailDomain);
    picked.push({ city, email: chosen, url: link });
    console.log(`${picked.length}. ${city} | ${chosen} | ${link}`);
    await wait(200);
    break;
  }
}

console.log('\nTOTAL', picked.length);
for (const p of picked) console.log(`${p.city}\t${p.email}\t${p.url}`);
