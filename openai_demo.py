import os
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
client = OpenAI()
response = client.responses.create(model=OPENAI_MODEL, input="Write a short bedtime story about a unicorn.")

print(response.output_text)