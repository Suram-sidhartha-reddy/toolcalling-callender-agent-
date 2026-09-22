import os

from dotenv import load_dotenv
from openai import OpenAI


# Load variables from .env
load_dotenv()

# Get Hugging Face token
hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise ValueError("HF_TOKEN not found in .env")


# Create OpenAI-compatible client
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_token,
)


# Send request to Hugging Face
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Explain what an AI agent is in exactly 3 sentences."
        }
    ],
)


# Print response
print("\nMODEL RESPONSE:\n")
print(response.choices[0].message.content)