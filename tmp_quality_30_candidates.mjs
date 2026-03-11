const candidates = [
  ['Argon Redovisningsbyrå','Stockholm','https://www.argon.se/'],
  ['Göteborgs Redovisningsbyrå','Göteborg','https://www.gotred.se/kontakt'],
  ['Redovisning 2000 AB','Malmö','https://redovisning2000.se/kontakt/'],
  ['Acreda','Örebro','https://acreda.se/'],
  ['Accont AB','Stockholm','https://www.accont.se/'],
  ['Multiekonomerna','Stockholm','https://multiekonomerna.se/'],
  ['Swed Redovisningsbyrå','Stockholm','https://www.swedredovisning.se/'],
  ['Accountmind','Stockholm','https://www.accountmind.se/'],
  ['Redovisningsbyrå Uppsala','Uppsala','https://redovisningsbyra-uppsala.se/kontakt-offert'],
  ['Klara Consulting','Västerås','https://klaraconsulting.se/kontakt/'],
  ['Aspia','Sverige','https://www.aspia.se/kontakt/'],
  ['Ludvig & Co','Sverige','https://www.ludvig.se/kontakt/'],
  ['Frejs Revisorer','Göteborg','https://www.frejsrevisorer.se/kontakt/'],
  ['RSM Sverige','Stockholm','https://www.rsm.global/sweden/sv/kontakta-oss'],
  ['Revideco','Göteborg','https://revideco.se/kontakt/'],
  ['SEVR Finance','Stockholm','https://sevrfinance.se/kontakt/'],
  ['PE Accounting','Stockholm','https://www.peaccounting.se/kontakt'],
  ['Qrev','Stockholm','https://qrev.se/kontakt/'],
  ['Wint','Göteborg','https://wint.se/kontakt/'],
  ['Grant Thornton Sverige','Stockholm','https://www.grantthornton.se/kontakta-oss/'],
  ['Baker Tilly Sverige','Sverige','https://www.bakertilly.se/kontakt'],
  ['LR Revision & Redovisning','Sverige','https://lrrevision.se/kontakt/'],
  ['BDO Sverige','Stockholm','https://www.bdo.se/sv-se/kontakta-oss'],
  ['Mazars Sverige','Stockholm','https://www.forvismazars.com/se/sv/kontakta-oss'],
  ['Adact Revisorer och Konsulter','Stockholm','https://adact.se/kontakt/'],
  ['Emvico','Malmö','https://emvico.se/kontakt/'],
  ['Moore Allegretto','Stockholm','https://www.moore-sverige.se/kontakt'],
  ['Parameter Revision','Stockholm','https://parameterrevision.se/kontakt/'],
  ['Sifferhjälpen','Jönköping','https://sifferhjalpen.se/kontakt/'],
  ['Ekonomernas Hus','Karlstad','https://ekonomernashus.se/kontakt/'],
  ['Lovisaredovisning','Linköping','https://lovisaredovisning.se/kontakt/'],
  ['HB Redovisning','Helsingborg','https://hbredovisning.se/kontakt/'],
  ['Cedrix Redovisning','Umeå','https://cedrix.se/kontakt/'],
  ['Dooer','Stockholm','https://dooer.com/sv/kontakt/'],
  ['Fortner','Stockholm','https://fortner.se/kontakt/'],
  ['Räkna med oss','Sundsvall','https://raknamedoss.se/kontakt/'],
  ['EkonomiRoslagen','Norrtälje','https://ekonomiroslagen.se/kontakt/'],
  ['Bokoredo','Borås','https://bokoredo.se/kontakt/'],
  ['Rallco','Luleå','https://rallco.se/kontakt/'],
  ['Auktoriserade Konsulter i Norr','Luleå','https://aknorr.se/kontakt/']
];

const rx = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
const bad = ['example.com','wixpress','sentry.io','loopia.com','loopia.se','loopia.no','loopia.rs','cloudflare'];

for (const [name, city, url] of candidates) {
  try {
    const t = await (await fetch(url, {headers:{'user-agent':'Mozilla/5.0'}})).text();
    const emails = [...new Set((t.match(rx)||[]).map(x=>x.toLowerCase()))]
      .filter(e => !bad.some(b => e.includes(b)));
    const chosen = emails.find(e => e.startsWith('info@') || e.startsWith('kontakt@') || e.startsWith('hej@') || e.startsWith('mail@')) || emails[0] || '';
    console.log([name, city, chosen, url].join('\t'));
  } catch {
    console.log([name, city, 'FETCH_FAIL', url].join('\t'));
  }
}
