#! /usr/bin/python
# task2.py - Parse html, extract and filter data from scrapped web pages with
# Beautiful Soup and Requests

import requests
from bs4 import BeautifulSoup

url = 'http://bbs.skykiwi.com/forum.php'
header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
baseTable = []

for i in range(1, 11):
    payload = {'mod': 'forumdisplay', 'fid': '17', 'page': str(i)}
    pages = requests.get(url, params=payload, headers=header)
    soup = BeautifulSoup(pages.text, "lxml")
    tbodyList = soup.select("tbody[id*=normalthread_]")
    for tbody in tbodyList:
        if tbody.select("span[title*=20]") != []:
            postTime = tbody.select("span[title*=20]")
            postDate = postTime[0]['title'].split()
            posts = tbody.select('a[class="xst"]')
            postTitle = posts[0].string
            postLink = 'http://bbs.skykiwi.com/' + posts[0]['href']
            baseTable.append([postTitle, postLink, postDate[0]])
        else:
            tbody.decompose()
print(len(baseTable))
