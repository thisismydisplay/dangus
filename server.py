from flask import Flask, request, jsonify
import requests
import re
import os

app = Flask(__name__)
bot_id = os.environ['GROUPME_BOT_ID']
def say(message):
    r = requests.post("https://api.groupme.com/v3/bots/post",
                      json={'bot_id': bot_id, 'text': message})
    print(r.status_code, r.reason)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/test', methods=['POST'])
def postmethod():
    data = request.get_json()
    
    if data['sender_type'] == 'bot':
        return ''
    elif not re.search('@dangus', data['text']):
        return ''
    elif re.search('you suck', data['text']):
        say("so do you")
    else:
        say("i don't do much yet")

    return ''
