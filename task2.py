#! /usr/bin/python
# task2.py - Parse html, extract and filter data from scrapped web pages with
# Beautiful Soup and Requests

import requests
from bs4 import BeautifulSoup

url = 'http://bbs.skykiwi.com/forum.php'
payload = {'mod': 'forumdisplay', 'fid': '17', 'page': '1'}
header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
r = requests.get(url, params=payload, headers=header)

soup = BeautifulSoup(r.text, "lxml")
tbodyList = soup.select("tbody[id*=normalthread_]")

baseTable = []
for tbody in tbodyList:
    posts = tbody.select('a[class="xst"]')
    postTitle = posts[0].string
    postLink = 'http://bbs.skykiwi.com/' + posts[0]['href']
    postTime = tbody.select("span[title*=20]")
    postDate = postTime[0]['title'].split()
    baseTable.append([postTitle, postLink, postDate[0]])
print(baseTable)
