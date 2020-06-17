import requests
import codecs
from bs4 import BeautifulSoup as bs


headers = {'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Referer': 'https://www.groupon.com/signup',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'es-ES,es;q=0.8'
           }
domain = 'https://work.ua'
url = 'https://work.ua/ru/jobs-kiev-python/'
resp = requests.get(url, headers=headers)
jobs = []
errors = []
if resp.status_code == 200:
    soup = bs(resp.content, 'html.parser')
    main_div = soup.find('div', id = "pjax-job-list")
    if main_div:
        div_list = main_div.find_all('div', attrs={'class': 'job-link'})
        for div in div_list:
            title = div.find('h2')
            href = title.a['href']
            content = div.p.text
            company = 'No name'
            logo = div.find('img')
            if logo:
                company = logo['alt']
            jobs.append({'title': title.text, 'url': domain+href,'description':content, 'company':company})
    else:
        errors.append({'url': url, 'title': "div does not exist"})
else:
    errors.append({'url':url, 'title': "page do not response"})
h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()
