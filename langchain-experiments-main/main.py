import os
import gunicorn
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request, jsonify
from functions import draft_email

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Set Slack API credentials
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
SLACK_BOT_USER_ID = os.environ.get("SLACK_BOT_USER_ID")

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

# Initialize the Flask app
# Flask is a web application framework written in Python
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# Set up the Slack API client
client = app.client

def my_function(text):
    """
    Custom function to process the text and return a response.
    In this example, the function converts the input text to uppercase.

    Args:
        text (str): The input text to process.

    Returns:
        str: The processed text.
    """
    response = text.upper()
    return response

@app.event("app_mention")
def handle_mentions(event, say):
    """
    Event listener for mentions in Slack.
    When the bot is mentioned, this function processes the text and sends a response.

    Args:
        event (dict): The event data received from Slack.
        say (callable): A function for sending a response to the channel.
    """
    text = event["text"]

    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip()

    say("Sure, I'll get right on that!")
    response = draft_email(text)
    say(response)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Endpoint to receive events from Slack.
    """

    # Convert the request data into JSON
    return handler.handle(request)

# Message to the screen when the app is running
@app.route("/")
def hello():
    return "Hello there! I'm a Slack bot."

# Run the Flask app
if __name__ == "__main__":
    flask_app.run()
