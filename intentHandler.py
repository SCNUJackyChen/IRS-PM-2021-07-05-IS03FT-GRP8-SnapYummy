########################################################
# FUNCTION TO COMMUNICATE WITH BACKEND - YOLO AND KG
#
########################################################

def browse_randomdish():
	return "Here is your randomDish:. \nPlease type the recipename you would like to have: "

def browse_byCuisineDietary(cuisineList, dietary):
	cuisine = ' '.join([str(elem) for elem in cuisineList])
	responsetxt = "You prefer " + cuisine + " cuisine and you have " + dietary + " constraints"
	return responsetxt

def cook_byIngredCuisineDietary(ingredList, cuisineList, dietary):
	ingredStr = ' '.join([str(elem) for elem in ingredList])
	cuisineStr = ' '.join([str(elem) for elem in cuisineList])
	responsetxt = "Ingredients: " + ingredStr + "\n\
					You prefer " + cuisineStr + " cuisine and you have " + dietary + " constraints"
	return responsetxt

def rec_instr(recipename):
	responsetxt = "Instructions for " + recipename + ": "
	return responsetxt

def rec_cooktime(recipename):
	responsetxt = "Cooking time for " + recipename + ": "
	return responsetxt

def rec_allInfo(recipename):
	instr = rec_instr(recipename)
	cooktime = rec_cooktime(recipename)
	responsetxt = instr + "\n" + cooktime
	return "You have choosen " + recipename + "\n" + responsetxt



##############################################################
# FUNCTION TO HANDLE INTENT
#
##############################################################

def Intent_Handler(intent_name, parameters):
	if intent_name == 'Browsing - random dishes':
		# Call random dish KG
		response_text = browse_randomdish()

	elif intent_name == 'Browsing - specific dishes - dietary_cuisine':
		# Get the cuisine and dietary
		cuisine = list(parameters["cuisine"])
		dietary = parameters["dietary"]
		# Call specific dish KG
		response_text = browse_byCuisineDietary(cuisine, dietary)

	elif intent_name == "cooking.ingredients.textmodify - no - dietary_cuisine":
		# Get the ingredients, cuisine and dietary
		ingred = list(parameters['ingredients'])
		cuisine = list(parameters["cuisine"])
		dietary = parameters["dietary"]
		# Call specific dish KG
		response_text = cook_byIngredCuisineDietary(ingred, cuisine, dietary)

	elif intent_name == 'Recipe':
		recipename = parameters["recipename"]
		response_text = rec_allInfo(recipename)

	elif intent_name == "Recipe - Instructions":
		recipename = parameters["recipename"]
		response_text = rec_instr(recipename)

	elif intent_name == "Recipe - CookingTime":
		recipename = parameters["recipename"]
		response_text = rec_cooktime(recipename)

	elif intent_name == "Recipe - recipeimg":
		recipename = parameters["recipename"]
		# To be updated
		response_text = recipename

	elif intent_name == "Recipe - ingredients":
		recipename = parameters["recipename"]
		# To be updated
		response_text = recipename

	#Showing more recipe results. Can be coming from random flow or specific flow
	elif intent_name == "Recipe - more_results":
		# Get the ingredients, cuisine and dietary
		ingred = list(parameters['ingredients'])
		cuisine = list(parameters["cuisine"])
		dietary = parameters["dietary"]

		#random - more

		# specific - more
		response_text = ""

	else:
		response_text = "Please try again. Unable to find a matching intent"

	return response_text