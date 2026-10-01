import os
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

client = OpenAI()
response = client.responses.create(model="gpt-6-astra", input="Write a short bedtime story about a unicorn.")

print(response.output_text)