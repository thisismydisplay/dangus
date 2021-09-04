from flask import request
import logging
import sys
import os
from aimodel import ai2
import numpy as np
import requests
import json
import re
import praw
# import os
import random
import threading

btc_previous = []
tired_responses = [
    "Don't let the nap get the best of you",
    "SLEEP",
    "dude",
    "idk have you tried more coffee?",
    "Each night, when I go to sleep, I die.",
]


bot_id = None
# app = Flask(__name__)
# bot_id = os.environ['PROD_GROUPME_BOT_ID']
# test_bot_id = os.environ['DEV_GROUPME_BOT_ID']
logger = logging.getLogger("gunicorn.error")


def make_pairs(corpus):
    for i in range(len(corpus) - 1):
        yield (corpus[i], corpus[i + 1])


def create_markov(corpus_path):
    text = open(corpus_path, encoding="utf8").read()
    split_text = text.split()
    for i, word in enumerate(split_text):
        if re.search("\[", word):
            split_text.pop(i)

    pairs = make_pairs(split_text)
    word_dict = {}

    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

    return word_dict


tay_dict = create_markov("all_tswift_lyrics.txt")
ts_dict = create_markov("tayspeare.txt")
shake_dict = create_markov("shakespeare.txt")


def markov_say(markov_dict):
    words = list(markov_dict.keys())
    first_word = np.random.choice(words)
    while first_word.islower():
        first_word = np.random.choice(words)
    chain = [first_word]
    n_words = random.randint(16, 42)

    for i in range(n_words):
        chain.append(np.random.choice(markov_dict[chain[-1]]))

    # logger.info(" ".join(chain))
    markov_chain = " ".join(chain)
    return markov_chain


def makemusic():
    with open("music.mp3", "w+") as fp:
        fp.write("this will be music for sure")


class Reddit:
    def __init__(self):
        self.reddit=praw.Reddit(
            client_id=os.environ.get("REDDIT_CLIENT_ID"),
            client_secret=os.environ.get("REDDIT_SECRET_TOKEN"),
            password=os.environ.get("REDDIT_PASSWORD"),
            user_agent="dangusbot/0.0.1",
            username=os.environ.get("REDDIT_USERNAME"),
        )

    def subreddit(self, subreddit_query):
        subreddit = self.reddit.subreddit(subreddit_query)
        top = list(subreddit.top(limit=1))[0]
        return (top.title, top.permalink)
class Bot:
    def __init__(self, bot_id, access_token, chat_filename):
        self.bot_id = bot_id
        self.access_token = access_token
        self.message_text = None
        self.other_bot_choice = None
        self.prompt_seed = None
        self.data = None
        self.has_alerted_recently = False
        self.group_id = None
        self.fetch_group_id()
        self.members = []
        self.reddit = Reddit()
        self.chat_filename = chat_filename

        logger.info(f"reddit= {self.reddit.subreddit('learnpython')}")

    def fetch_group_id(self):
        params = {"token":self.access_token}
        resp = requests.get("https://api.groupme.com/v3/bots", params=params)
        data = resp.json()
        
        for bot in data["response"]:
            
            if bot["bot_id"] == self.bot_id:
                self.group_id = bot["group_id"]

        if self.group_id == None:
            raise Exception("No group id found searching groupme")


    def run(self):
        self.btc_trawler()
        self.get_current_members()

    def route(self):
        self.assign_flask_info()
        self.store_grouptext()
        num = random.randint(1, 10)
        if self.data["sender_type"] == "bot":
            return ""
        elif re.search("tired", self.data["text"]):
            self.say(np.random.choice(tired_responses))
        elif not re.search("@dangus", self.data["text"]):
            return ""

        elif re.search("subreddit (\w+)", self.data["text"]):
            sub_call = re.search("subreddit (\w+)", self.data["text"])
            title, permalink = self.reddit.subreddit(sub_call.group(1))
            self.say(title)

        elif re.search("you suck", self.data["text"]):
            self.say("so do you")
        elif re.search("make music", self.data["text"]):
            makemusic()
        elif re.search(r"\bbtc\b|\bbitcoin\b", self.data["text"], re.IGNORECASE):
            btc_data = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")

            test_btc = json.loads(btc_data.text)
            logger.info(test_btc["bpi"]["USD"]["rate"])
            test_btc_usd = test_btc["bpi"]["USD"]["rate_float"]

            format_float_test_btc_usd = "{:,.2f}".format(test_btc_usd)
            self.say(f"Current value of Bitcoin in USD is ${format_float_test_btc_usd}")

        # elif num < 2:
        # pass
        # respond = ai.generate_one(prompt=prompt_seed, max_length=40, temperature=1.6)
        # self.say(respond)
        elif num < 3:
            respond = ai2.generate_one(
                prompt=self.prompt_seed, max_length=40, temperature=1.4
            )
            self.say(respond)
            logger.info("ai")
            logger.info(respond)
        # self.say(ts_say())
        # logger.info('t-s')
        elif num < 5:
            self.say(markov_say(ts_dict))
        elif num < 6:
            self.say("Who cares?")
        elif num < 7:
            # TODO: decide where to use ai vs markov
            # respond=ai.generate_one(prompt=prompt_seed, max_length=40, temperature=1.6)
            # self.say(respond)
            self.say(markov_say(shake_dict))
        elif num < 8:
            self.say("¯\_(ツ)_/¯")
        elif num < 9:
            self.say(markov_say(tay_dict))
        elif self.other_bot_choice == "@dingus" and num > 8:
            self.say(f"I don't know, maybe you should talk to {self.other_bot_choice}")
        elif self.message_text == "":
            self.say("I don't know, maybe you should talk to ")
            self.say(self.other_bot_choice)
        else:
            self.say("I don't know, maybe Dongus can help?")
            self.say(f"{self.other_bot_choice} ##{self.message_text}")

        return ""

    
    
    def store_grouptext(self):
        text_to_store = self.message_text
        text_to_store = text_to_store.replace("@dingus", "")
        text_to_store = text_to_store.replace("@dongus", "")
        for nickname in self.members:
            text_to_store = text_to_store.replace(f"@{nickname}", "")
        text_to_store = text_to_store.lstrip(' ')
        if self.data["sender_type"] == "bot":
            return ""
        else:
            with open(self.chat_filename, "a+") as chat_record:
                chat_record.write(text_to_store +"\n")
    
    def say(self, message):
        try:
            r = requests.post(
                "https://api.groupme.com/v3/bots/post",
                json={"bot_id": self.bot_id, "text": message},
            )
            logger.info(r.status_code, r.reason)
        except:
            logger.info("unexpected error:", sys.exc_info()[0])

    def btc_trawler(self):
        global btc_previous
        btc_data = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")

        new_btc = json.loads(btc_data.text)
        btc_previous.append(new_btc)
        logger.info(btc_previous)
        if len(btc_previous) > 60:
            old_btc = btc_previous.pop(0)
            new_usd = new_btc["bpi"]["USD"]["rate_float"]
            logger.info(new_usd)
            old_usd = old_btc["bpi"]["USD"]["rate_float"]
            logger.info(old_usd)
            logger.info(new_usd - old_usd)
            logger.info((new_usd - old_usd) / old_usd)
            percent_change = (new_usd - old_usd) / old_usd
            logger.info(percent_change)
            format_float_test_btc_usd = "{:,.2f}".format(new_usd)
            if percent_change > 0.03:
                logger.info("inside >")
                self.send_alert(
                    f"Value of Bitcoin has changed {'{:.2%}'.format(percent_change)}"
                    + f" in the last hour and is now USD is ${format_float_test_btc_usd}"
                )
            elif percent_change < -0.03:
                logger.info("inside <")
                self.send_alert(
                    f"Value of Bitcoin has changed {'{:.2%}'.format(percent_change)}"
                    + f" in the last hour and is now USD is ${format_float_test_btc_usd}"
                )
        t = threading.Timer(60, self.btc_trawler)
        t.start()

    def get_current_members(self):
        params = {"token":self.access_token}
        group_resp= requests.get(f"https://api.groupme.com/v3/groups/{self.group_id}", params=params)
        
        member_list = group_resp.json()["response"]["members"]
        self.members = list(map(lambda x: x["nickname"], member_list))
        logger.info(f"self.members = {self.members}")
        t = threading.Timer(3600, self.get_current_members)
        t.start()


    def send_alert(self, message):
        if self.has_alerted_recently:
            return

        logger.info(message)
        self.say(message)
        self.has_alerted_recently = True

        # Only alert every 4 hours
        def reset_alert():
            self.has_alerted_recently = False

        t = threading.Timer(60 * 60 * 4, reset_alert)
        t.start()

    def assign_flask_info(self):
        global btc_previous
        data = request.get_json()
        # logger.info(f"data= {data}")
        other_bots = ["@dingus", "@dongus"]
        other_bot_choice = random.choice(other_bots)
        self.message_text = data["text"]
        self.message_text = self.message_text.replace("@dangus", "")
        message_text_to_seed = self.message_text.split()
        # message_text_length = len(message_text)
        if len(message_text_to_seed) != 0:
            prompt_seed = random.choice(message_text_to_seed)
        else:
            prompt_seed = "You"
        # prompt_seed = random.choice(message_text)
        # prompt_seed = str(np.random.choice(message_text.split()))
        logger.info(prompt_seed)
        self.prompt_seed = prompt_seed
        self.other_bot_choice = other_bot_choice
        self.data = data
