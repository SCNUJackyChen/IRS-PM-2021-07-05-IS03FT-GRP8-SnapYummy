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
	msg_type = telepot.glance(msg)[0]

	if msg_type == 'photo':  # when a photo comes in, handle it without dialogflow
		# img = bot.getFile(msg['photo'][-1]['file_id'])
		# print(msg['photo'][-1])
		# print(img)

		bot.download_file(msg['photo'][-1]['file_id'], './images/' + msg['photo'][-1]['file_id'] + '.png')  # download
		# the image sent by users
		print('a photo received')

	elif msg_type == 'text':  # when a text comes in, call dialogflow API to detect the intent
		query_sentence = str(msg['text'])
		intent_name = detect_intent_texts(df_agentID, msg['chat']['id'], query_sentence, 'en-US')
		print(intent_name)


bot = telepot.Bot(telegram_botTOKEN)
MessageLoop(bot, reqHandler).run_as_thread()

while 1:
	time.sleep(10)
