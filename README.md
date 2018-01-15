# Info-Collection-of-Second-hand-Market
Hello, Welcome!

# Introduction
This is a Python program that can be used to collect customized information of second-hand goods from bbs.skykiwi.com according to user's demands and to send mail notifications to the user with the collected information.
For non-commercial use only.

# Implementation
- Send HTTP requests with Requests library - refer to task1.py
- Scrape Webpages and extract data from HTML with BeautifulSoup library - refer to task2.py
- Send mails via API provided by Mailgun service https://www.mailgun.com/ - refer to task3.py

# How to use
- Configuration
First configure the followings in config.py
keywords - a list of keywords of the second-hand goods that you want to subscribe
API_URL, API_Key, from_Domain - Mailgun service configuration with your account
mailList - your email address(es) to receive the information
- Run
Run the program "SecondHandInfo.py" and then just wait for the useful and extract info mails to come!
The program will collect the posts in the last 7 days, which hit any of the keywords interest you in the post title or body, from the second-hand market page from bbs.skykiwi.com.
