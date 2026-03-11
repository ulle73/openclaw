import { setTimeout as wait } from 'node:timers/promises';

const cities = ['Stockholm','Goteborg','Malmo','Uppsala','Vasteras','Orebro','Linkoping','Sundsvall','Umea','Lulea'];
const results = [];

const emailRegex = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;

for (const city of cities) {
  const q = encodeURIComponent(`redovisningsbyra ${city} kontakt epost`);
  const searchUrl = `https://html.duckduckgo.com/html/?q=${q}`;
  let html = '';
  try {
    html = await (await fetch(searchUrl, { headers: { 'user-agent': 'Mozilla/5.0' } })).text();
  } catch (e) {
    console.log(city, '=> search fail');
    continue;
  }

  const links = [];
  const re = /<a[^>]+class="result__a"[^>]+href="([^"]+)"/g;
  let m;
  while ((m = re.exec(html)) !== null && links.length < 10) {
    let href = m[1].replaceAll('&amp;', '&');
    const mm = href.match(/uddg=([^&]+)/);
    if (mm) href = decodeURIComponent(mm[1]);
    links.push(href);
  }

  let found = false;
  for (const link of links) {
    if (!link.startsWith('http')) continue;
    try {
      const t = await (await fetch(link, { headers: { 'user-agent': 'Mozilla/5.0' } })).text();
      const emails = [...new Set((t.match(emailRegex) || []).filter(e => !e.includes('example.com') && !e.includes('wixpress')) )];
      if (emails.length) {
        const email = emails.sort((a,b)=>a.length-b.length)[0];
        results.push({ city, email, link });
        console.log(`${city} => ${email} | ${link}`);
        found = true;
        break;
      }
    } catch {}
    await wait(200);
  }
  if (!found) console.log(city, '=> none');
}

console.log('\nTOTAL', results.length);
for (const r of results) console.log(`${r.city}\t${r.email}\t${r.link}`);
