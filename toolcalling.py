import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise ValueError("HF_TOKEN not found")


client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_token,
)


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
            "Cancel my meeting with Rahul tomorrow."
        )
    }
]



response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)



assistant_message = response.choices[0].message

print("\n=== MODEL RESPONSE ===")
print(assistant_message)


if assistant_message.tool_calls:

    print("\n=== TOOL CALL REQUESTED ===")

    for tool_call in assistant_message.tool_calls:

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        print(f"\nTool: {tool_name}")
        print(f"Arguments: {arguments}")

        if tool_name == "create_event":

            result = create_event(
                title=arguments["title"],
                date=arguments["date"],
                time=arguments["time"]
            )

            print("\nTool result:")
            print(result)

else:

    print("\nModel did not request a tool.")

    print("\nModel said:")
    print(assistant_message.content)

