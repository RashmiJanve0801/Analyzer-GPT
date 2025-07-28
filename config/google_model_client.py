from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

import os
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def get_model_client():
    google_model_client = OpenAIChatCompletionClient(
        model='gemini-2.0-flash'
    )

    return google_model_client