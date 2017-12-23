#! /usr/bin/python
# task1.py - Make a request and get target information of the request and
# response with Requests

import requests

url = 'http://bbs.skykiwi.com/forum.php'
payload = {'mod': 'forumdisplay', 'fid': '17'}
header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

r = requests.get(url, params=payload, headers=header)
print(r.url)
print(r.request.headers)
print(r.request.body)
print(r.headers)
print(r.content)
