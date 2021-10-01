########################################################
# FUNCTION TO COMMUNICATE WITH BACKEND - YOLO AND KG
#
########################################################

from py2neo.data import Record
from Neo4j import neo
from Conversation import Conversation

USERS = {}

def browse_randomdish():
	return "Here is your randomDish:. \nPlease type the recipename you would like to have: "

def browse_byCuisineDietary(cuisineList, dietary):
	cuisine = ' '.join([str(elem) for elem in cuisineList])
	responsetxt = "You prefer " + cuisine + " cuisine and you have " + dietary + " constraints"
	return responsetxt

def cook_byIngredCuisineDietary(ingredList, cuisineList, dietary, chat_id):
	ingredStr = ' '.join([str(elem) for elem in ingredList])
	cuisineStr = ' '.join([str(elem) for elem in cuisineList])
	responsetxt = "Ingredients: " + ingredStr + "\n\
					You prefer " + cuisineStr + " cuisine and you have " + dietary + " constraints" + "\n"
	if 'no' in dietary.lower():
		dietary = None
	recipes = neo.getRecipes(list(ingredList), dietary=dietary)
	for i, r in enumerate(recipes):
		responsetxt += '/' + str(i) + ' ' + r['Name'] + '\n'
	USERS[chat_id] = Conversation(chat_id, recipes)
	return responsetxt

def list_selection(recipename):
	responsetxt = recipename + '\n'
	responsetxt +=  '1. /instruction \n' + \
		            '2. /time for cooking \n' + \
					'3. /ingredients \n' + \
					'4. /all information \n'
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
		response_text = browse_randomdish()

	elif intent_name == 'Browsing - specific dishes - dietary_cuisine':
		# Get the cuisine and dietary
		cuisine = set(parameters["cuisine"])
		dietary = parameters["dietary"]
		# Call specific dish KG
		response_text = browse_byCuisineDietary(cuisine, dietary)

	elif intent_name == "cooking.ingredients.textmodify - no - dietary_cuisine":
		# Get the ingredients, cuisine and dietary
		ingred = set(parameters['ingredients'])
		cuisine = set(parameters["cuisine"])
		dietary = parameters["dietary"]
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
		# To be updated
		response_text = recipename

	elif intent_name == "Recipe - Ingredients":
		recipename = parameters["recipename"]
		recipeID = int(parameters["RID"])
		# To be updated
		response_text = rec_ingrd(recipeID, recipename, chat_id)

	#Showing more recipe results. Can be coming from random flow or specific flow
	elif intent_name == "Recipe - more_results":
		# Get the ingredients, cuisine and dietary
		ingred = set(parameters['ingredients'])
		cuisine = set(parameters["cuisine"])
		dietary = parameters["dietary"]

		#random - more

		# specific - more
		response_text = ""

	else:
		response_text = "Please try again. Unable to find a matching intent"

	return response_text