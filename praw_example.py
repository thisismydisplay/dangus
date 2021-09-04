# This script is used to demonstrate the reddit API. It also serves as a test of
# your REDIT_ACCESS_TOKEN enviorment variable, which is required to run this
# script.

import config
import os
import requests
import praw
from pprint import pprint

reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_SECRET_TOKEN"),
    password=os.environ.get("REDDIT_PASSWORD"),
    user_agent="dangusbot/0.0.1",
    username=os.environ.get("REDDIT_USERNAME"),
)

print(reddit.user.me())

for submission in reddit.subreddit("learnpython").hot(limit=10):
    pprint(submission.__dict__)

