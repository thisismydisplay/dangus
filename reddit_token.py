# Code borrowed with major modifications from
# https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
# 
# Most important modification is that we are using a completely different API
# route to get the access token.

import config
import os
import requests

CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
SECRET = os.environ.get("REDDIT_SECRET_TOKEN")

# See https://github.com/reddit-archive/reddit/wiki/OAuth2#application-only-oauth
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET)

data = {"grant_type": "client_credentials"}

# setup our header info, which gives reddit a brief description of our app
headers = {"User-Agent": "DangusBot/0.0.1"}

# send our request for an OAuth token
res = requests.post(
    "https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers
)

# convert response to JSON and pull access_token value
TOKEN = res.json()["access_token"]

print("Token request successful. Add the following to your .env file:")
print(f"REDDIT_ACCESS_TOKEN='{TOKEN}'")
