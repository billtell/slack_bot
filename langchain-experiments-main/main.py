import os
import gunicorn
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request, jsonify
from functions import draft_email

# # Load environment variables from .env file
load_dotenv(find_dotenv())

# Set Slack API credentials
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
SLACK_BOT_USER_ID = os.environ.get("SLACK_BOT_USER_ID")

# # Initialize the Slack app
# app = App(token=SLACK_BOT_TOKEN)

# # Initialize the Flask app
# # Flask is a web application framework written in Python
# flask_app = Flask(__name__)
# handler = SlackRequestHandler(app)

# Set up the Flask app
app = Flask(__name__)


# Set up the Slack API client
client = WebClient(token=SLACK_BOT_TOKEN)

#get port from environment variable or choose 3000 as local default
port = int(os.environ.get("PORT", 3000))


# def get_bot_user_id():
#     """
#     Get the bot user ID using the Slack API.
#     Returns:
#         str: The bot user ID.
#     """
#     try:
#         # Initialize the Slack client with your bot token
#         slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
#         response = slack_client.auth_test()
#         return response["user_id"]
#     except SlackApiError as e:
#         print(f"Error: {e}")

# def my_function(text):
#     """
#     Custom function to process the text and return a response.
#     In this example, the function converts the input text to uppercase.

#     Args:
#         text (str): The input text to process.

#     Returns:
#         str: The processed text.
#     """
#     response = text.upper()
#     return response


# @app.event("app_mention")
# def handle_mentions(body, say):
#     """
#     Event listener for mentions in Slack.
#     When the bot is mentioned, this function processes the text and sends a response.

#     Args:
#         body (dict): The event data received from Slack.
#         say (callable): A function for sending a response to the channel.
#     """
#     text = body["event"]["text"]

#     mention = f"<@{SLACK_BOT_USER_ID}>"
#     text = text.replace(mention, "").strip()

#     say("Sure, I'll get right on that!")
#     # response = my_function(text)
#     response = draft_email(text)
#     say(response)


# @flask_app.route("/slack/events", methods=["POST"])
# def slack_events():
#     """
#     Endpoint to receive events from Slack.
#     """

#     # Convert the request data into JSON
#     return handler.handle(request)


# #message to the screen when the app is running
# @flask_app.route("/")
# def hello():
#     return "Hello there! I'm a Slack bot."

# # Run the Flask app
# if __name__ == "__main__":
#     flask_app.run()

# Define a route to handle Slack events
@app.route("/slack/events", methods=["POST"])
def handle_slack_event():
    # Parse the incoming request
    payload = request.json
    event = payload["event"]

    # Handle the event
    if event["type"] == "message" and "hello" in event["text"]:
        try:
            # Send a response back to Slack
            response = client.chat_postMessage(
                channel=event["channel"],
                text="Hello, world!"
            )
            return jsonify(response)
        except SlackApiError as e:
            return jsonify({"error": str(e)}), 500

# Define a route to handle Slack commands
@app.route("/slack/commands", methods=["POST"])
def handle_slack_command():
    # Parse the incoming request
    payload = request.form
    command = payload["command"]
    text = payload["text"]
    user_id = payload["user_id"]

    # Handle the command
    if command == "/echo":
        try:
            # Send a response back to Slack
            response = client.chat_postMessage(
                channel=user_id,
                text=text
            )
            return jsonify(response)
        except SlackApiError as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=port)






