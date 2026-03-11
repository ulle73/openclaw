const firms = [
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
  ['Revideco','Göteborg','https://revideco.se/kontakt/'],
  ['Parameter Revision','Stockholm','https://parameterrevision.se/kontakt/'],
  ['Sifferhjälpen','Jönköping','https://sifferhjalpen.se/kontakt/'],
  ['Ekonomernas Hus','Karlstad','https://ekonomernashus.se/kontakt/'],
  ['Rallco','Luleå','https://rallco.se/kontakt/'],
  ['EkonomiRoslagen','Norrtälje','https://ekonomiroslagen.se/kontakt/'],
  ['Bokoredo','Borås','https://bokoredo.se/kontakt/'],
  ['Lovisaredovisning','Linköping','https://lovisaredovisning.se/kontakt/'],
  ['HB Redovisning','Helsingborg','https://hbredovisning.se/kontakt/'],
  ['Cedrix Redovisning','Umeå','https://cedrix.se/kontakt/'],
  ['Räkna med oss','Sundsvall','https://raknamedoss.se/kontakt/'],
  ['Adact Revisorer och Konsulter','Stockholm','https://adact.se/kontakt/'],
  ['SEVR Finance','Stockholm','https://sevrfinance.se/kontakt/'],
  ['PE Accounting','Stockholm','https://www.peaccounting.se/kontakt'],
  ['Qrev','Stockholm','https://qrev.se/kontakt/'],
  ['Wint','Göteborg','https://wint.se/kontakt/'],
  ['Ludvig & Co','Sverige','https://www.ludvig.se/kontakt/'],
  ['Grant Thornton Sverige','Stockholm','https://www.grantthornton.se/kontakta-oss/'],
  ['Baker Tilly Sverige','Sverige','https://www.bakertilly.se/kontakt'],
  ['BDO Sverige','Stockholm','https://www.bdo.se/sv-se/kontakta-oss'],
  ['Mazars Sverige','Stockholm','https://www.forvismazars.com/se/sv/kontakta-oss'],
  ['RSM Sverige','Stockholm','https://www.rsm.global/sweden/sv/kontakta-oss'],
  ['Frejs Revisorer','Göteborg','https://www.frejsrevisorer.se/kontakt/'],
  ['Moore Sverige','Stockholm','https://www.moore-sverige.se/kontakt'],
  ['LR Revision','Sverige','https://lrrevision.se/kontakt/'],
  ['Talenom','Sverige','https://www.talenom.se/kontakt/'],
  ['BQ Redovisning','Stockholm','https://bqredovisning.se/'],
  ['Saldo Redovisning','Stockholm','https://saldoredovisning.se/'],
  ['Wahlgrens Redovisningsbyrå','Stockholm','https://www.wahlgrensredovisning.se/'],
  ['Viredo','Stockholm','https://viredo.se/'],
  ['Vil Accounting','Stockholm','https://www.vilaccounting.se/'],
  ['KAM Redovisning','Stockholm','https://www.kam.nu/']
];

const rx = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
const bad = ['example.com','wixpress','sentry.io','loopia.com','loopia.se','loopia.no','loopia.rs','png','jpg','jpeg','webp','svg'];

function chooseEmail(emails, domain) {
  if (!emails.length) return '';
  const pref = emails.find(e => e.startsWith('info@') || e.startsWith('kontakt@') || e.startsWith('hej@') || e.startsWith('mail@'));
  if (pref) return pref;
  const domainMatch = emails.find(e => domain && e.endsWith('@' + domain));
  return domainMatch || emails[0];
}

for (const [name, city, url] of firms) {
  try {
    const u = new URL(url);
    const domain = u.hostname.replace(/^www\./,'').toLowerCase();
    const html = await (await fetch(url, {headers:{'user-agent':'Mozilla/5.0'}})).text();
    let emails = [...new Set((html.match(rx) || []).map(x => x.toLowerCase()))];
    emails = emails.filter(e => !bad.some(b => e.includes(b)));
    const chosen = chooseEmail(emails, domain);
    console.log([name, city, chosen || 'NO_EMAIL', url].join('\t'));
  } catch {
    console.log([name, city, 'FETCH_FAIL', url].join('\t'));
  }
}
