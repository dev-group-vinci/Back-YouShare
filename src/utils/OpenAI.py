import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


class OpenAI:

    def __init__(self):
        pass

    @staticmethod
    def moderateContent(text):
        response = openai.Moderation.create(
            input=text
        )
        return response["results"][0]["flagged"]
