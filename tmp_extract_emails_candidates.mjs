const candidates = [
  ['Argon Redovisningsbyrå','Stockholm','https://www.argon.se/'],
  ['Accountmind','Stockholm','https://www.accountmind.se/'],
  ['Göteborgs Redovisningsbyrå','Göteborg','https://www.gotred.se/kontakt'],
  ['Acreda','Örebro','https://acreda.se/'],
  ['Redovisningsbyrå Uppsala','Uppsala','https://redovisningsbyra-uppsala.se/kontakt-offert'],
  ['Klara Consulting','Västerås','https://klaraconsulting.se/kontakt/vara-kontor/vasteras/redovisningsbyra/'],
  ['Aspia Linköping','Linköping','https://www.aspia.se/kontakt/linkoping/'],
  ['BQ Redovisning','Stockholm','https://bqredovisning.se/'],
  ['Accont','Stockholm','https://www.accont.se/'],
  ['Swed Redovisning','Stockholm/Skärholmen','https://www.swedredovisning.se/'],
  ['Multiekonomerna','Stockholm','https://multiekonomerna.se/'],
  ['Saldo Redovisning','Stockholm','https://saldoredovisning.se/'],
  ['Wahlgrens Redovisningsbyrå','Stockholm','https://www.wahlgrensredovisning.se/'],
  ['Talenom Sverige','Sverige','https://www.talenom.se/kontakt/'],
  ['Ludvig & Co','Sverige','https://www.ludvig.se/kontakt/'],
];

const rx = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
for (const [name, city, url] of candidates) {
  try {
    const t = await (await fetch(url, { headers: { 'user-agent': 'Mozilla/5.0' } })).text();
    const emails = [...new Set((t.match(rx) || []).filter(e => !e.includes('example.com') && !e.includes('wixpress') && !e.endsWith('.png') && !e.endsWith('.jpg')) )];
    console.log('\n'+name+' | '+city+' | '+url);
    console.log(emails.slice(0,6).join(', '));
  } catch (e) {
    console.log('\n'+name+' | '+city+' | '+url);
    console.log('FETCH_FAIL');
  }
}
