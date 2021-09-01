# This script is used to demonstrate the reddit API. It also serves as a test of
# your REDIT_ACCESS_TOKEN enviorment variable, which is required to run this
# script.

import config
import os
import requests
from pprint import pprint

TOKEN = os.environ.get("REDDIT_ACCESS_TOKEN")

if TOKEN is None:
    print("You must set the REDDIT_ACCESS_TOKEN environment variable.")
    exit(1)

# add authorization to our headers dictionary
headers = {"User-Agent": "DangusBot/0.0.1", "Authorization": f"bearer {TOKEN}"}

# # while the token is valid (~2 hours) we just add headers=headers to our requests
res = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)

# tell us about ourself
pprint("GET https://oauth.reddit.com/api/v1/me result:")
pprint(res.json())

# Use the reddit API to get the first 10 posts from the cryptocurrency subreddit
params = {"limit": 5, "article": "pfi20y", "sort": "top", "depth": 1}
res = requests.get(
    "https://oauth.reddit.com/r/cryptocurrency/comments/article", headers=headers, params=params
)

pprint("GET https://oauth.reddit.com/r/cryptocurrency/hot/ result:")
pprint(res.json())
print("\n\n\n\n")
pprint("Top post of /r/cryptocurrency/ is:")
pprint(res.json()["data"]["children"][0]["data"])
print("\n\n\n\n")
pprint("Title of top post of /r/cryptocurrency/ is:")
pprint(res.json()["data"]["children"][0]["data"]["title"])
