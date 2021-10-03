########################################################
# FUNCTION TO COMMUNICATE WITH BACKEND - YOLO AND KG
#
########################################################

from typing import ChainMap
from py2neo.data import Record
from Neo4j import neo
from Conversation import Conversation

USERS = {}

def browse_randomdish(chat_id):
	recipes = neo.browser()
	responsetxt = "Here is your randomDish: \n"
	for i, r in enumerate(recipes):
		responsetxt += '/' + str(i) + ' ' + r['Name'] + '\n'
	responsetxt += '/more dishes'
	if chat_id not in USERS:
		USERS[chat_id] = Conversation(chat_id, recipes)
	else:
		USERS[chat_id].recipes = recipes
	
	return responsetxt

def browse_byCuisineDietary(cuisine, dietaryList, chat_id):
	dietaryStr = ' '.join([str(elem) for elem in dietaryList])
	responsetxt = "You prefer " + cuisine + " and you have " + dietaryStr + " constraints \n"

	if 'no' in dietaryList[0].lower():
		dietaryList = None
	if 'no' in cuisine.lower():
		cuisine = None
	recipes = neo.browser(cuisine=cuisine, dietaryList=dietaryList)
	if chat_id not in USERS:
		USERS[chat_id] = Conversation(chat_id, recipes)
	else:
		USERS[chat_id].recipes = recipes
	
	for i, r in enumerate(recipes):
		responsetxt += '/' + str(i) + ' ' + r['Name'] + '\n'
	responsetxt += '/more dishes'
	return responsetxt

def cook_byIngredCuisineDietary(ingredList, cuisine, dietaryList, chat_id):
	ingredStr = ' '.join([str(elem) for elem in ingredList])
	dietaryStr = ' '.join([str(elem) for elem in dietaryList])

	responsetxt = "Ingredients: " + ingredStr + "\n\
					You prefer " + cuisine + " cuisine and you have " + dietaryStr + " constraints" + "\n"
	if 'no' in dietaryList[0].lower():
		dietaryList = None
	if 'no' in cuisine.lower():
		cuisine = None
	skip = 0
	if chat_id in USERS:
		USERS[chat_id].search_time += 1
		skip = USERS[chat_id].search_time

	recipes = neo.getRecipes(list(ingredList), cuisine=cuisine, dietaryList=dietaryList, skip=skip)
	for i, r in enumerate(recipes):
		responsetxt += '/' + str(i) + ' ' + r['Name'] + '\n'
	responsetxt += '/more dishes'
	if chat_id not in USERS:
		USERS[chat_id] = Conversation(chat_id, recipes)
	else:
		USERS[chat_id].recipes = recipes

	return responsetxt

def list_selection(recipename):
	responsetxt = recipename + '\n'
	responsetxt +=  '1. /instruction \n' + \
		            '2. /time for cooking \n' + \
					'3. /ingredients \n' + \
					'4. /img \n' + \
					'5. /all information \n'
	return responsetxt

def rec_ingrd(recipeID, recipename, chat_id):
	id = USERS[chat_id].recipes[recipeID]["RecipeId"]
	responsetxt = "【Ingredients for " + recipename + "】: \n"
	ingrs = neo.getIngredient(id, recipename)
	ingrs = list(set(ingrs))
	responsetxt += '\n'.join(ingrs)
	# print(ingrs)
	# print(responsetxt)
	return responsetxt

def rec_instr(recipeID, recipename, chat_id):
	responsetxt = "【Instructions for " + recipename + "】: \n"
	instr = USERS[chat_id].recipes[recipeID]["RecipeInstructions"]
	responsetxt += instr.replace("'", '').replace('[', '').replace(']', '') + '\n'
	return responsetxt

def rec_cooktime(recipeID, recipename, chat_id):
	responsetxt = "【Cooking time for " + recipename + "】: \n"
	responsetxt += str(USERS[chat_id].recipes[recipeID]["CookTime"]) + '\n'
	return responsetxt

def rec_allInfo(recipeID, recipename, chat_id):
	instr = rec_instr(recipeID, recipename, chat_id)
	cooktime = rec_cooktime(recipeID, recipename, chat_id)
	ingrd = rec_ingrd(recipeID, recipename, chat_id)
	responsetxt = instr + "\n" + cooktime + '\n' + ingrd
	return "You have choosen " + recipename + "\n" + responsetxt



##############################################################
# FUNCTION TO HANDLE INTENT
#
##############################################################

def Intent_Handler(intent_name, parameters, chat_id):
	if intent_name == 'Browsing - random dishes':
		# Call random dish KG
		response_text = browse_randomdish(chat_id)

	elif intent_name == 'Browsing - specific dishes - dietary_cuisine':
		# Get the cuisine and dietary
		cuisine = parameters["cuisine"]
		dietary = list(set(parameters["dietary"]))
		# Call specific dish KG
		response_text = browse_byCuisineDietary(cuisine, dietary, chat_id)

	elif intent_name == "cooking.ingredients.textmodify - no - dietary_cuisine":
		# Get the ingredients, cuisine and dietary
		ingred = parameters['ingredients']
		cuisine = parameters["cuisine"]
		dietary = list(set(parameters["dietary"]))
		# Call specific dish KG
		response_text = cook_byIngredCuisineDietary(ingred, cuisine, dietary, chat_id)

	elif intent_name == 'Recipe':
		recipename = parameters["recipename"]
		response_text = list_selection(recipename)

	elif intent_name == "Recipe - AllInfo":
		recipename = parameters["recipename"]
		recipeID = int(parameters["RID"])
		response_text = rec_allInfo(recipeID, recipename, chat_id)

	elif intent_name == "Recipe - Instructions":
		recipename = parameters["recipename"]
		recipeID = int(parameters["RID"])
		response_text = rec_instr(recipeID, recipename, chat_id)

	elif intent_name == "Recipe - CookingTime":
		recipename = parameters["recipename"]
		recipeID = int(parameters["RID"])
		response_text = rec_cooktime(recipeID, recipename, chat_id)

	elif intent_name == "Recipe - recipeimg":
		recipename = parameters["recipename"]
		recipeID = int(parameters["RID"])

		# return an img of a recipe
		if USERS[chat_id].recipes[recipeID]["Images"] != '[]':
			img_url = USERS[chat_id].recipes[recipeID]["Images"]
			img_url = img_url[1:-1].split('\n')[0][1:-1]
			print(img_url)
			response_text = ['here is the image of ' + recipename, img_url]
		else:
			response_text = 'no image of ' + recipename

	elif intent_name == "Recipe - Ingredients":
		recipename = parameters["recipename"]
		recipeID = int(parameters["RID"])
		# To be updated
		response_text = rec_ingrd(recipeID, recipename, chat_id)

	#Showing more recipe results. Can be coming from random flow or specific flow
	elif intent_name == "Recipe - more_results":
		print(parameters['ingredients'])
		print(parameters['cuisine'])
		print(parameters['dietary'])
		if parameters['ingredients'] != '':
			ingred = parameters['ingredients']
			cuisine = parameters["cuisine"]
			dietary = list(set(parameters["dietary"]))
			response_text = cook_byIngredCuisineDietary(ingred, cuisine, dietary, chat_id)
		elif parameters['cuisine'] != '':
			cuisine = parameters["cuisine"]
			dietary = list(set(parameters["dietary"]))
			response_text = browse_byCuisineDietary(cuisine, dietary, chat_id)
		else:
			response_text = browse_randomdish(chat_id)

	else:
		response_text = "Please try again. Unable to find a matching intent"

	return response_text