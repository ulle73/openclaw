const urls = [
  'https://klaraconsulting.se/kontakt/',
  'https://www.aspia.se/kontakt/',
  'https://www.aspia.se/kontakt/linkoping/',
  'https://revideco.se/kontakt/',
  'https://www.ludvig.se/kontakt/',
  'https://www.grantthornton.se/kontakta-oss/',
  'https://www.bdo.se/sv-se/kontakta-oss',
  'https://www.bakertilly.se/kontakt',
  'https://www.rsm.global/sweden/sv/kontakta-oss',
  'https://www.frejsrevisorer.se/kontakt/',
  'https://www.moore-sverige.se/kontakt',
  'https://adact.se/kontakt/',
  'https://parameterrevision.se/kontakt/',
  'https://sifferhjalpen.se/kontakt/',
  'https://ekonomernashus.se/kontakt/'
];
const rx = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
const bad = ['example.com','wixpress','sentry.io','loopia','png','jpg','jpeg','webp','svg'];
for (const url of urls) {
  try {
    const t = await (await fetch(url,{headers:{'user-agent':'Mozilla/5.0'}})).text();
    let emails = [...new Set((t.match(rx)||[]).map(x=>x.toLowerCase()))];
    emails = emails.filter(e => !bad.some(b => e.includes(b)));
    console.log('\nURL\t'+url);
    console.log(emails.join('\n'));
  } catch {
    console.log('\nURL\t'+url+'\nFETCH_FAIL');
  }
}
