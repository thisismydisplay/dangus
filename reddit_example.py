import config
import os
import requests
from pprint import pprint

TOKEN = os.environ.get("REDDIT_ACCESS_TOKEN")

# add authorization to our headers dictionary
headers = {"User-Agent": "DangusBot/0.0.1", **{"Authorization": f"bearer {TOKEN}"}}

# # while the token is valid (~2 hours) we just add headers=headers to our requests
res = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)

pprint("GET https://oauth.reddit.com/api/v1/me result:")
pprint(res.json())
