const cities = ['stockholm','goteborg','malmo','uppsala','vasteras','orebro','linkoping','helsingborg','jonkoping','norrkoping','lund','umea','gavle','boras','sodertalje','eskilstuna','halmstad','vaxjo','karlstad','sundsvall','ostersund','lulea','kalmar','skelleftea','kristianstad','falun','trollhattan','nykoping','varberg','visby'];
const rx = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
for (const c of cities) {
  const urls = [
    `https://redovisningsbyra-${c}.se/kontakt-offert`,
    `https://redovisningsbyra-${c}.se/kontakt/`,
    `https://redovisningsbyra-${c}.se/`
  ];
  let found=''; let used='';
  for (const u of urls) {
    try {
      const t = await (await fetch(u,{headers:{'user-agent':'Mozilla/5.0'}})).text();
      const emails = [...new Set((t.match(rx)||[]).map(x=>x.toLowerCase()))].filter(e=>!e.includes('example.com')&&!e.includes('loopia')&&!e.includes('wixpress'));
      if (emails.length) { found = emails[0]; used=u; break; }
    } catch {}
  }
  if (found) console.log(`${c}\t${found}\t${used}`);
}
