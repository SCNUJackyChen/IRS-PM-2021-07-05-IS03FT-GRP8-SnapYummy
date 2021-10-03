import telepot
import time
import os
from dfCaller import *
from yoloCaller import *
from intentHandler import *
import random
from telepot.loop import MessageLoop


# from pprint import pprint

# global settings
df_agentID = 'recipeagent-swjn'
telegram_botTOKEN = '1983955379:AAEhEf0VbCtA_AVSBfHfFMmDuA_HWqNaDsI'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "recipeagent.json"


def reqHandler(msg):  # directly monitor telegram
	(msg_type, _, chat_id) = telepot.glance(msg)
	# welcome_msg = ["Good day, Welcome to RecipePR. If you are looking for \n1. /cooking based on your ingredients, or \n\
	# 2. Browsing for /recipe to cook, \nYou are coming to the right place! \n How can I assist you today?", "Hello, Welcome to RecipePR.\n\
	# For cooking based on your ingredients, click /cooking\nFor leisure browsing of the recipe to cook, click /recipe"]
	# rdm = random.randint(0, 1)
	# bot.sendMessage(chat_id, str(welcome_msg[rdm]))

	if msg_type == 'photo':  # when a photo comes in, handle it without dialogflow
		# img = bot.getFile(msg['photo'][-1]['file_id'])
		# print(msg['photo'][-1])
		# print(img)
		img_dir = './images/' + str(chat_id) + str(time.time()) + '.png'
		bot.download_file(msg['photo'][-1]['file_id'], img_dir)  # download the image sent by users
		detected_ingredients = detect_image(img_dir)  # send the img to YOLO and get results

		# whenever user upload an image, send '/cooking' to DF -> reset the workflow
		detect_intent_texts(df_agentID, msg['chat']['id'], '/cooking', 'en-US')
		(intent_name, df_response, parameters) = detect_intent_texts(df_agentID, msg['chat']['id'], ', '.join(detected_ingredients),
																	 'en-US')
		print(intent_name, "-", df_response, "-", parameters)
		bot.sendMessage(chat_id, df_response)



	elif msg_type == 'text':  # when a text comes in, call dialogflow API to detect the intent
		query_sentence = str(msg['text'])
		if query_sentence[0] == '/' and query_sentence[1:].isdigit():
			id = int(query_sentence[1:])
			recipe_name = USERS[chat_id].recipes[id]["Name"]
			query_sentence = 'Got recipe for ' + recipe_name
			USERS[chat_id].set_pick(id)
		# elif query_sentence[0:2] == '/b' and query_sentence[2:].isdigit():
		# 	id = int(query_sentence[2:])
		# 	recipe_name = USERS[chat_id].recipes[id]["Name"]
		# 	query_sentence = 'Got recipe for ' + recipe_name	
		# 	USERS[chat_id].set_pick(id)
		elif query_sentence == '/instruction':
			query_sentence = 'instructions'
		elif query_sentence == '/time':
			query_sentence = 'cooking time'
		elif query_sentence == '/ingredients':
			query_sentence = 'show me the ingredients for this dish'
		elif query_sentence == '/all':
			query_sentence = 'show all'
		elif query_sentence == '/more':
			query_sentence = 'more results'
		elif query_sentence == '/img':
			query_sentence = 'show me the recipe image'
		
		(intent_name, df_response, parameters) = detect_intent_texts(df_agentID, msg['chat']['id'], query_sentence,
																	 'en-US')
		print(intent_name, "-", df_response, "-", parameters)
		if df_response == "":
			if chat_id in USERS.keys():
				id = USERS[chat_id].get_pick()
				if id is not None:
					parameters["recipename"] = USERS[chat_id].recipes[id]["Name"]
					parameters["RID"] = id
			response_text = Intent_Handler(intent_name, parameters, chat_id)
		else:
			response_text = df_response

		if type(response_text) == list:  # an image url is contained
			bot.sendMessage(chat_id, response_text[0])
			bot.sendPhoto(chat_id, response_text[1])
		else:
			bot.sendMessage(chat_id, response_text)


bot = telepot.Bot(telegram_botTOKEN)
MessageLoop(bot, reqHandler).run_as_thread()

while 1:
	time.sleep(10)
