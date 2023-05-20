from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import openai

load_dotenv(find_dotenv())

# functions for the bot to respond to

#summarize
#answer
#draft email
#provide a story
#provide a poem
#provide a joke
#provide a quote
#provide a fact
#compare news stories from around the world
#compare news stories from different sources

#use openai to generate a story
def generate_story():
    return openai.Completion.create(
        engine="davinci",
        prompt="Once upon a time",
        temperature=0.7,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )

#use openai to generate a poem
def generate_poem():
    return openai.Completion.create(
        engine="davinci",
        prompt="Roses are red, violets are blue",
        temperature=0.7,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )

#use openai to generate a joke
def generate_joke():
    return openai.Completion.create(
        engine="davinci",
        prompt="Why did the chicken cross the road?",
        temperature=0.7,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )

#use openai to generate a quote
def generate_quote():
    return openai.Completion.create(
        engine="davinci",
        prompt="The meaning of life is",
        temperature=0.7,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )

#use openai to generate a fact
def generate_fact():
    return openai.Completion.create(
        engine="davinci",
        prompt="The world is",
        temperature=0.7,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )

class eventHandler:
    def __init__(self):
        self.chatbot = ChatOpenAI()
        self.chatbot.load()
        self.chatbot.set_prompt(ChatPromptTemplate())
        self.chatbot.set_system_message_prompt(SystemMessagePromptTemplate())
        self.chatbot.set_human_message_prompt(HumanMessagePromptTemplate())
        self.chatbot.set_cha

    def handle_it(self, request):
        """
        Route for handling Slack events.
        This function passes the incoming HTTP request to the SlackRequestHandler for processing.

        Returns:
            Response: The result of handling the request.
        """
        # Create an instance of SlackRequestHandler.
        # The SlackRequestHandler class contains several helper functions for verifying requests and getting data from the request.
        slack_handler = SlackRequestHandler()

        # Verify the request token.
        # This will abort the request early if the token does not match.
        slack_handler.verify_token(request)

        # Get the event data from the request.
        # This will abort the request early if the event type is not "event_callback".
        event_data = slack_handler.get_event_data(request)

        # Get the event type from the event data.
        event_type = slack_handler.get_event_type(event_data)

        # Get the user ID of the user who triggered the event.
        user_id = slack_handler.get_user_id(event_data)

        # Get the channel ID of the channel where the event was triggered.
        channel_id = slack_handler.get_channel_id(event_data)

        # Get the text from the event that was triggered.
        text = slack_handler.get_text(event_data)

        #if text is equal to 'summarize'
        if text == 'summarize':