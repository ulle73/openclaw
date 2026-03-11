import re, requests, bs4, urllib.parse, time
cities=['Stockholm','Goteborg','Malmo','Uppsala','Vasteras','Orebro','Linkoping','Sundsvall','Umea','Lulea']
headers={'User-Agent':'Mozilla/5.0'}
results=[]
for city in cities:
    q=f'redovisningsbyra {city} kontakt epost'
    url='https://html.duckduckgo.com/html/?q='+urllib.parse.quote(q)
    try:
        html=requests.get(url,headers=headers,timeout=20).text
    except Exception as e:
        print('search fail',city,e); continue
    soup=bs4.BeautifulSoup(html,'html.parser')
    links=[]
    for a in soup.select('a.result__a')[:10]:
        href=a.get('href') or ''
        m=re.search(r'uddg=([^&]+)',href)
        if m:
            href=urllib.parse.unquote(m.group(1))
        links.append(href)
    found=False
    for link in links:
        if not link.startswith('http'):
            continue
        try:
            t=requests.get(link,headers=headers,timeout=20).text
        except Exception:
            continue
        emails=set(re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',t))
        emails=[e for e in emails if 'example.com' not in e.lower() and 'wixpress' not in e.lower()]
        if emails:
            email=sorted(emails,key=len)[0]
            results.append((city,link,email))
            print(city,'=>',email,'|',link)
            found=True
            break
        time.sleep(0.2)
    if not found:
        print(city,'=> none')
print('\nTOTAL',len(results))
for city,link,email in results:
    print(f'{city}\t{email}\t{link}')
