import telepot
import time
import os
from dfCaller import *
from telepot.loop import MessageLoop

# from pprint import pprint

# global settings
df_agentID = 'irs-recipeagent-eumg'
telegram_botTOKEN = '2046937306:AAGEaymdXBYLeCKzydhBq5TN0kUQVC8pcKs'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ".\irs-recipeagent-eumg-e91a34c1c2bf.json"


def reqHandler(msg):  # directly monitor telegram
	(msg_type, _, chat_id) = telepot.glance(msg)

	if msg_type == 'photo':  # when a photo comes in, handle it without dialogflow
		# img = bot.getFile(msg['photo'][-1]['file_id'])
		# print(msg['photo'][-1])
		# print(img)

		bot.download_file(msg['photo'][-1]['file_id'], './images/' + msg['photo'][-1]['file_id'] + '.png')  # download
		# the image sent by users
		bot.sendMessage(chat_id, 'a photo received (returned by script)')

	elif msg_type == 'text':  # when a text comes in, call dialogflow API to detect the intent
		query_sentence = str(msg['text'])
		(intent_name, default_response) = detect_intent_texts(df_agentID, msg['chat']['id'], query_sentence, 'en-US')
		bot.sendMessage(chat_id, 'your intent is: ' + intent_name + '(returned by calling dialogflow API)')
		bot.sendMessage(chat_id, 'the pre-set response in DF is: ' + default_response)


bot = telepot.Bot(telegram_botTOKEN)
MessageLoop(bot, reqHandler).run_as_thread()

while 1:
	time.sleep(10)
