
def browse_randomdish():
	return "Here is your randomDish:. \nPlease type the recipename you would like to have: "

def browse_byCuisineDietary(cuisineList, dietary):
	cuisine = ' '.join([str(elem) for elem in cuisineList])
	responsetxt = "You prefer " + cuisine + " cuisine and you have " + dietary + " constraints"
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
	return responsetxt

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

	elif intent_name == 'Recipe':
		recipename = parameters["recipename"]
		response_text = rec_allInfo(recipename)

	elif intent_name == "Recipe - Instructions":
		recipename = parameters["recipename"]
		response_text = rec_instr()

	else:
		response_text = "Please try again. Unable to find a matching intent"

	return response_text