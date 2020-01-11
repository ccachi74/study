'''
torrentmax.net 사이트에서 마그넷 사이트 검색
'''
import requests
from bs4 import BeautifulSoup

kword = input('검색어 입력 : ')
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
url = 'https://torrentmax.net/search?url=https%3A%2F%2Ftorrentmax.net%2Fsearch&stx={}'.format(kword)
r = requests.get(url, headers=header)
bs = BeautifulSoup(r.content, 'lxml')
divs = bs.select('div.media-heading')

for d in divs:
    alink = d.select('a')[0]
    title = alink.text
    href = alink.get('href')

    r = requests.get(href)
    bs = BeautifulSoup(r.content, 'lxml')
    all_links = bs.select('div.panel.panel-default')
    for g in all_links:
        g_links = g.select('a')
        for a in g_links:
            a_link = a.get('href')
            if a_link is None:
                continue
            if a_link.find('magnet:?') >= 0:
                print(title, href, a_link)

