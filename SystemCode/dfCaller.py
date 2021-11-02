# from flask import Flask, request, make_response, jsonify
# import requests
from google.cloud import dialogflow


# app = Flask(__name__)

def detect_intent_texts(project_id, session_id, text,
						language_code):  # sent query to dialogflow to get intent & default response

	session_client = dialogflow.SessionsClient()

	session = session_client.session_path(project_id, session_id)
	# print("Session path: {}\n".format(session))

	text_input = dialogflow.TextInput(text=text, language_code=language_code)

	query_input = dialogflow.QueryInput(text=text_input)

	response = session_client.detect_intent(
		request={"session": session, "query_input": query_input}
	)

	# print("=" * 20)
	# print("Query text: {}".format(response.query_result.query_text))
	# print(
	# 	"Detected intent: {} (confidence: {})\n".format(
	# 		response.query_result.intent.display_name,
	# 		response.query_result.intent_detection_confidence,
	# 	)
	# )
	# print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))

	return [str(response.query_result.intent.display_name), str(response.query_result.fulfillment_text),
			response.query_result.parameters]
