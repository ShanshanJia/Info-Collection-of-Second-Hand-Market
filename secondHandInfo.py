#! /usr/bin/python
# secondHandInfo.py - This is the main program.

import requests
from bs4 import BeautifulSoup
import config


# Scrape all the posts in the scope of pages, return a list of posts with post title, hyperlink and date
def scrapePosts(url, header, frpage, topage):
    postTable = []
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
                postTable.append([postTitle, postLink, postDate[0]])
            # Remove post data earlier than one week
            else:
                tbody.decompose()
    return postTable


# Dig into post detail page and scrape the body text, append the corresponding body data to the post table
def scrapeBodies(postTable):
    fullPostTable = []
    # Request post detail pages by the post links
    for i in range(len(postTable)):
        bodyPage = requests.get(postTable[i][1], headers=config.header)
        soup = BeautifulSoup(bodyPage.text, "lxml")
        # Remove post status data from the body text
        postInfo = soup.find(class_='pstatus')
        if postInfo:
            postInfo.decompose()
        # Pull body text of the first main message only
        tdList = soup.select('td[class="t_f"]')
        bodyText = tdList[0].get_text()
        # Return a full post table with post title, hyperlink, date and post body
        fullPostTable.append([postTable[i][0], postTable[i][1], postTable[i][2], bodyText])
    return fullPostTable


# Given a list of keywords, filter the posts if the post title or body contains any of the keyword in the list
def hitKeywords(tList):
    result = False
    for key in config.keywords:
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


# Send email with text to the recipient(s) using Mailgun API and service
def sendMail(mailText, mailList):
    return requests.post(config.API_URL, auth=("api", config.API_Key), data={"from": config.from_Domain, "to": mailList, "subject": config.subject, "text": mailText})


# The main function
def main():
    postTable = scrapePosts(config.url, config.header, config.frpage, config.topage)
    fullTable = scrapeBodies(postTable)
    filterTable = filter(hitKeywords, fullTable)
    filterText = table2Text(filterTable)
    mailResult = sendMail(filterText, config.mailList)
    print(mailResult)


if __name__ == "__main__":
    main()
