#! /usr/bin/python
# Task3: Send mails using Mailgun services and API, with customized mail subjuect and content to the recipients

import requests

API_URL = ""
API_Key = ""
from_Domain = ""
to_List = ["", ""]
subject = "Hello"
text = "Testing!"

requests.post(API_URL, auth=("api", API_Key), data={"from": from_Domain, "to": to_List, "subject": subject, "text": text})
