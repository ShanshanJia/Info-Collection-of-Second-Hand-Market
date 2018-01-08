#! /usr/bin/python
# task2.py - Parse html, extract and filter data from scrapped web pages with Beautiful Soup and Requests.
# Collect the posts of second-hand product posted within one week that the post title or body contains any of the product demanded by user
import requests
from bs4 import BeautifulSoup

url = 'http://bbs.skykiwi.com/forum.php'
header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
keywords = ['内存', 'iphone', '吸尘器']


# Scrape all the posts in the scope of pages, return a list of posts with post title, hyperlink and date
def scrapePosts(url, header, frpage, topage):
    baseTable = []
    # Parse all the pages
    for i in range(frpage, topage + 1):
        payload = {'mod': 'forumdisplay', 'fid': '17', 'page': str(i)}
        page = requests.get(url, params=payload, headers=header)
        soup = BeautifulSoup(page.text, "lxml")
        # Pull all post data from "normalthread_..." <tbody>
        tbodyList = soup.select("tbody[id*=normalthread_]")
        for tbody in tbodyList:
            # Select the posts within one week, where the latest post time is in the title of the span
            if tbody.select("span[title*=20]"):
                postTime = tbody.select("span[title*=20]")
                # Extract post date from span title e.g."2017-01-01 12:00:00"
                postDate = postTime[0]['title'].split()
                # Pull post title and link from <a>
                posts = tbody.select('a[class="xst"]')
                postTitle = posts[0].string
                postLink = 'http://bbs.skykiwi.com/' + posts[0]['href']
                baseTable.append([postTitle, postLink, postDate[0]])
            # Remove post data earlier than one week
            else:
                tbody.decompose()
    return baseTable


# Dig into post detail page and scrape the body text, append the corresponding body data to the post table
def scrapeBodies(baseTable):
    extendTable = []
    # Request post detail pages by the post links
    for i in range(len(baseTable)):
        bodyPage = requests.get(baseTable[i][1], headers=header)
        soup = BeautifulSoup(bodyPage.text, "lxml")
        # Remove post status data from the body text
        postInfo = soup.find(class_='pstatus')
        if postInfo:
            postInfo.decompose()
        # Pull body text of the first main message only
        tdList = soup.select('td[class="t_f"]')
        bodyText = tdList[0].get_text()
        # Return a full post table with post title, hyperlink, date and post body
        extendTable.append([baseTable[i][0], baseTable[i][1], baseTable[i][2], bodyText])
    return extendTable


# Given a list of keywords, filter the posts if the post title or body contains any of the keyword in the list
def hitKeywords(tList):
    result = False
    for key in keywords:
        if (key in tList[0]) or (key in tList[3]):
            result = True
            break
    return result


# Transform the post table to text messages that can be printed or mailed to user as the mail text
def table2Text(fTable):
    text = ['Here are some posts you might be interested in:']
    for post in fTable:
        text.append(post[0] + ', ' + post[1] + ', ' + post[2])
    fullText = '\n'.join(text)
    return fullText


postTable = scrapePosts(url, header, 1, 10)
fullTable = scrapeBodies(postTable)
filterTable = filter(hitKeywords, fullTable)
filterText = table2Text(filterTable)
print(filterText)
