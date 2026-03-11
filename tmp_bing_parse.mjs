const q = encodeURIComponent('redovisningsbyrå sundsvall kontakt e-post');
const u = 'https://www.bing.com/search?q=' + q;
const t = await (await fetch(u, { headers: { 'user-agent': 'Mozilla/5.0' } })).text();
const matches = [...t.matchAll(/<a href="(https?:\/\/[^\"]+)"/g)].map(x => x[1]);
console.log(matches.slice(0, 30));
