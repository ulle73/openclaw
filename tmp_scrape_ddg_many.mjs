import { setTimeout as wait } from 'node:timers/promises';

const cities = ['Helsingborg','Jönköping','Norrköping','Lund','Gävle','Borås','Södertälje','Eskilstuna','Halmstad','Växjö','Karlstad','Östersund','Kalmar','Skellefteå','Kristianstad','Falun','Trollhättan','Nyköping','Varberg','Visby'];
const emailRegex = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
const bad = ['loopia','sentry.io','example.com','wixpress'];

for (const city of cities) {
  const q = encodeURIComponent(`redovisningsbyrå ${city} kontakt email`);
  const surl = `https://html.duckduckgo.com/html/?q=${q}`;
  let html='';
  try { html = await (await fetch(surl,{headers:{'user-agent':'Mozilla/5.0'}})).text(); }
  catch { console.log(city+'\tSEARCH_FAIL'); continue; }
  if (html.includes('Unfortunately, bots use DuckDuckGo')) { console.log(city+'\tDDG_BLOCK'); continue; }

  const links=[];
  const re=/<a[^>]+class="result__a"[^>]+href="([^"]+)"/g;
  let m;
  while ((m=re.exec(html)) && links.length<10) {
    let href=m[1].replaceAll('&amp;','&');
    const mm=href.match(/uddg=([^&]+)/);
    if (mm) href=decodeURIComponent(mm[1]);
    links.push(href);
  }

  let out='NONE';
  for (const link of links) {
    if (!link.startsWith('http')) continue;
    try {
      const t = await (await fetch(link,{headers:{'user-agent':'Mozilla/5.0'}})).text();
      let emails=[...new Set((t.match(emailRegex)||[]).map(x=>x.toLowerCase()))];
      emails=emails.filter(e=>!bad.some(b=>e.includes(b)));
      if (emails.length) { out = `${emails[0]}\t${link}`; break; }
    } catch {}
    await wait(150);
  }
  console.log(`${city}\t${out}`);
  await wait(300);
}
