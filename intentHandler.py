
def browse_randomdish():
    return "randomDish"

def browse_byCuisineDietary(cuisineList, dietary):
    cuisine = ' '.join([str(elem) for elem in cuisineList])
    responsetxt = "You prefer " + cuisine + " cuisine and you have " + dietary + " constraints"
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

	else:
		response_text = "Please try again. Unable to find a matching intent"

	return response_text