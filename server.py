from flask import Flask, request, jsonify
import requests
import json
import re
import os
import random
import numpy as np

tay = open('all_tswift_lyrics.txt', encoding='utf8').read()
print(tay)
corpus = tay.split()
print(corpus)

app = Flask(__name__)
bot_id = os.environ['PROD_GROUPME_BOT_ID']
test_bot_id = os.environ['DEV_GROUPME_BOT_ID']

for i, word in enumerate(corpus):
    if re.search("\[", word):
        corpus.pop(i)
print(corpus)

def make_pairs(corpus):
    for i in range(len(corpus) - 1):
        yield (corpus[i], corpus[i + 1])


pairs = make_pairs(corpus)

word_dict = {}

for word_1, word_2 in pairs:
    if word_1 in word_dict.keys():
        word_dict[word_1].append(word_2)
    else:
        word_dict[word_1] = [word_2]

def taysay():
    first_word = np.random.choice(corpus)
    chain = [first_word]
    n_words = random.randint(20,48)

    for i in range(n_words):
        chain.append(np.random.choice(word_dict[chain[-1]]))

    print(' '.join(chain))
    taychain=' '.join(chain)
    return taychain

print(taysay())


def say(message):
    r = requests.post("https://api.groupme.com/v3/bots/post",
                      json={'bot_id': bot_id, 'text': message})
    print(r.status_code, r.reason)

def dev_say(message):
    r = requests.post("https://api.groupme.com/v3/bots/post",
                      json={'bot_id': test_bot_id, 'text': message})
    print(r.status_code, r.reason)

@app.route("/main", methods=['POST'])
def main_route():
    data = request.get_json()
    num=random.randint(1,10)
    other_bots = ['@dingus', '@dongus']
    other_bot_choice = random.choice(other_bots)
    message_text = data['text']
    message_text = message_text.replace('@dangus', '')

    if data['sender_type'] == 'bot':
        return ''
    elif not re.search('@dangus', data['text']):
        return ''
    elif re.search('you suck', data['text']):
        say("so do you")
    elif re.search(r"\bbtc\b|\bbitcoin\b", data['text'], re.IGNORECASE):
        btc_data = requests.get(
            "https://api.coindesk.com/v1/bpi/currentprice.json")
        btc_price = btc_data.text
        test_btc = json.loads(btc_data.text)
        print(test_btc['bpi']['USD']['rate'])
        test_btc_usd = test_btc['bpi']['USD']['rate_float']
        # test_btc_usd = float(test_btc_usd)
        format_float_test_btc_usd = "{:,.2f}".format(test_btc_usd)
        say(f"Current value of Bitcoin in USD is ${format_float_test_btc_usd}")
        # pairs = test_btc['bpi']['USD'].items()
        # for key, value in pairs:
        #    print(value)
    elif num<9:
        say(taysay())
    elif other_bot_choice == '@dingus' and num>8:
        say(
            f"I don't know, maybe you should talk to {other_bot_choice}")
    elif message_text == '':
        say("I don't know, maybe you should talk to ")
        say(other_bot_choice)
    else:
        say("I don't know, maybe Dongus can help?")
        say(f"{other_bot_choice} ##{message_text}")

    return ''


@app.route('/test', methods=['POST'])
def test_route():
    data = request.get_json()
    num=random.randint(1,10)
    other_bots = ['@dingus', '@dongus']
    other_bot_choice = random.choice(other_bots)
    message_text = data['text']
    message_text = message_text.replace('@dangus', '')

    if data['sender_type'] == 'bot':
        return ''
    elif not re.search('@dangus', data['text']):
        return ''
    elif re.search('you suck', data['text']):
        dev_say("so do you")
    elif re.search(r"\bbtc\b|\bbitcoin\b", data['text'], re.IGNORECASE):
        btc_data = requests.get(
            "https://api.coindesk.com/v1/bpi/currentprice.json")
        btc_price = btc_data.text
        test_btc = json.loads(btc_data.text)
        print(test_btc['bpi']['USD']['rate'])
        test_btc_usd = test_btc['bpi']['USD']['rate_float']
        # test_btc_usd = float(test_btc_usd)
        format_float_test_btc_usd = "{:,.2f}".format(test_btc_usd)
        dev_say(f"Current value of Bitcoin in USD is ${format_float_test_btc_usd}")
        # pairs = test_btc['bpi']['USD'].items()
        # for key, value in pairs:
        #    print(value)
    elif num<9:
        dev_say(taysay())
    elif other_bot_choice == '@dingus' and num>8:
        dev_say(
            f"I don't know, maybe you should talk to {other_bot_choice}")
    elif message_text == '':
        dev_say("I don't know, maybe you should talk to ")
        dev_say(other_bot_choice)
    else:
        dev_say("I don't know, maybe Dongus can help?")
        dev_say(f"{other_bot_choice} ##{message_text}")

    return ''
