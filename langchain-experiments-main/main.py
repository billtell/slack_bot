import os
import gunicorn
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request, jsonify
from functions import draft_email

# get the tokens from the config vars
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

# Initialize the Flask app
# Flask is a web application framework written in Python
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# Set up the Slack API client
client = app.client

# #create a route for the slash command
# @flask_app.route("/slack/message_actions", methods=["POST"])
# def message_actions():
#     # Parse the request payload
#     form_json = request.form["payload"]
#     payload = json.loads(form_json)
#     # Check to see what the user's selection was and update the message
#     selection = payload["actions"][0]["value"]
#     if selection == "yes":
#         response = "Great! I'll send you a message to get started."
#     elif selection == "no":
#         response = "Okay, maybe next time."
#     else:
#         response = "Oops, something went wrong."
#     return jsonify(
#         replace_original=True,
#         text=response
#     )

# # Create a route slack events 
# @flask_app.route("/slack/events", methods=["POST"])
# def slack_events():
#     # Parse the request payload
#     form_json = request.form["payload"]
#     payload = json.loads(form_json)
#     # Check to see what the user's selection was and update the message
#     selection = payload["actions"][0]["value"]
#     if selection == "yes":
#         response = "Great! I'll send you a message to get started."
#     elif selection == "no":
#         response = "Okay, maybe next time."
#     else:
#         response = "Oops, something went wrong."
#     return jsonify(
#         replace_original=True,
#         text=response
#     )

# Message to the screen when the app is running
@flask_app.route("/")
def hello():
    return "Hello there! I'm a Slack bot."

# Run the Flask app
if __name__ == "__main__":
    flask_app.run(debug=True)
