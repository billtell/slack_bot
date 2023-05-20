import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request, Response
from functions import draft_email, answer_question

# Load environment variables from .env file
load_dotenv(find_dotenv())



# Initialize the Slack app
app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Initialize the Flask app
# Flask is a web application framework written in Python
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

def get_bot_user_id():
    """
    Get the bot user ID using the Slack API.
    Returns:
        str: The bot user ID.
    """
    try:
        # Initialize the Slack client with your bot token
        slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
        response = slack_client.auth_test()
        return response["user_id"]
    except SlackApiError as e:
        print(f"Error: {e}")

# Get the bot user ID
BOT_USER_ID = get_bot_user_id()

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
def handle_mentions(body, say):
    """
    Event listener for mentions in Slack.
    When the bot is mentioned, this function processes the text and sends a response.

    Args:
        body (dict): The event data received from Slack.
        say (callable): A function for sending a response to the channel.
    """
    text = body["event"]["text"]

    #get the user id of the person who mentioned the bot
    user_id = body["event"]["user"]
    #convert the user id to user handle
    user_id = f"<@{user_id}>"

    mention = f"<@{BOT_USER_ID}>"
    text = text.replace(mention, "").strip()

    say(f"Sure, I'll get right on that, {user_id}!")
    response = answer_question(text)
    # response = draft_email(text)
    say(response)

@flask_app.route('/', methods=['GET'])
def hello_world():
    return Response('Hello, World! I am a slack bot!', mimetype='text/plain')

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Route for handling Slack events.
    This function passes the incoming HTTP request to the SlackRequestHandler for processing.

    Returns:
        Response: The result of handling the request.
    """
    return handler.handle(request)


# Run the Flask app
if __name__ == "__main__":
    flask_app.run(debug=True)
