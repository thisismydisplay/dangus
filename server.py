import config
from flask import Flask
from development import Bot as TestBot
from production import Bot as MainBot
import os
import logging

logger = logging.getLogger("gunicorn.error")
app = Flask(__name__)
app.logger.handlers = logger.handlers
logger.info("I'm working")
test_bot_id = os.environ['DEV_GROUPME_BOT_ID']
bot_id = os.environ['PROD_GROUPME_BOT_ID']
access_token =os.environ['GROUPME_ACCESS_TOKEN']

test_bot = TestBot(test_bot_id, access_token, "chathistory_dev.txt")
test_bot.run()
main_bot = MainBot(bot_id, access_token, "chathistory_prod.txt")
main_bot.run()

@app.route('/test', methods=['POST'])
def development():
    return test_bot.route()

@app.route("/main", methods=['POST'])
def production():
    return main_bot.route()

