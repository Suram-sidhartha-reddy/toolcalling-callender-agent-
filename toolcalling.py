import os
import json

from dotenv import load_dotenv
from openai import OpenAI


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise ValueError("HF_TOKEN not found")


# --------------------------------------------------
# 2. Create Hugging Face client
# --------------------------------------------------

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_token,
)


# --------------------------------------------------
# 3. Define our actual Python function
# --------------------------------------------------

def create_event(title: str, date: str, time: str):
    """
    Create a calendar event.

    For now this is only a fake implementation.
    Later this will communicate with Google Calendar.
    """

    print("\n=== CREATE EVENT TOOL EXECUTED ===")

    print(f"Title : {title}")
    print(f"Date  : {date}")
    print(f"Time  : {time}")

    return {
        "success": True,
        "message": f"Event '{title}' created successfully."
    }


# --------------------------------------------------
# 4. Describe the function to the LLM
# --------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "create_event",

            "description": (
                "Create a calendar event with a title, date and time."
            ),

            "parameters": {
                "type": "object",

                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the calendar event"
                    },

                    "date": {
                        "type": "string",
                        "description": (
                            "Event date in YYYY-MM-DD format"
                        )
                    },

                    "time": {
                        "type": "string",
                        "description": (
                            "Event time in 24-hour HH:MM format"
                        )
                    }
                },

                "required": [
                    "title",
                    "date",
                    "time"
                ]
            }
        }
    }
]


# --------------------------------------------------
# 5. User request
# --------------------------------------------------

messages = [
    {
        "role": "system",
        "content": (
            "You are a calendar assistant. "
            "Use the available calendar tools when the user "
            "asks you to perform calendar actions."
        )
    },

    {
        "role": "user",
        "content": (
            "Create a meeting with Rahul tomorrow at 4 PM."
        )
    }
]


# --------------------------------------------------
# 6. Ask the model whether a tool is needed
# --------------------------------------------------

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)


# --------------------------------------------------
# 7. Get the assistant message
# --------------------------------------------------

assistant_message = response.choices[0].message

print("\n=== MODEL RESPONSE ===")
print(assistant_message)


# --------------------------------------------------
# 8. Check whether the model requested a tool
# --------------------------------------------------

if assistant_message.tool_calls:

    print("\n=== TOOL CALL REQUESTED ===")

    for tool_call in assistant_message.tool_calls:

        print("Tool name:")
        print(tool_call.function.name)

        print("\nArguments:")
        print(tool_call.function.arguments)


else:

    print("\nModel did not request a tool.")

    print("\nModel said:")
    print(assistant_message.content)