import os
import json

from dotenv import load_dotenv
from openai import OpenAI


# ==================================================
# 1. Load environment variables
# ==================================================

load_dotenv()

hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise ValueError("HF_TOKEN not found in .env")




client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_token,
)




def create_event(title: str, date: str, time: str):

    print("\n[TOOL] Creating calendar event...")

    print(f"Title: {title}")
    print(f"Date : {date}")
    print(f"Time : {time}")

    # Fake calendar operation for now
    # Google Calendar will be connected later.

    return {
        "success": True,
        "event_id": "event_12345",
        "title": title,
        "date": date,
        "time": time,
    }




tools = [
    {
        "type": "function",
        "function": {
            "name": "create_event",

            "description": (
                "Create a calendar event with a title, "
                "date and time."
            ),

            "parameters": {
                "type": "object",

                "properties": {

                    "title": {
                        "type": "string",
                        "description": "Title of the event"
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
                            "Event time in HH:MM 24-hour format"
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
            "Use calendar tools when the user asks "
            "you to create calendar events."
        )
    },

    {
        "role": "user",
        "content": (
            "Create a meeting with Rahul tomorrow at 4 PM."
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



if assistant_message.tool_calls:

    print("\n[LLM] Tool call requested.")

    

    messages.append(assistant_message)



    for tool_call in assistant_message.tool_calls:

        function_name = tool_call.function.name

        function_args = json.loads(
            tool_call.function.arguments
        )

        print("\n[LLM] Requested tool:")
        print(function_name)

        print("\n[LLM] Arguments:")
        print(function_args)



        if function_name == "create_event":

            result = create_event(
                title=function_args["title"],
                date=function_args["date"],
                time=function_args["time"],
            )



        else:

            result = {
                "success": False,
                "error": f"Unknown tool: {function_name}"
            }


        

        messages.append({

            "role": "tool",

            "tool_call_id": tool_call.id,

            "name": function_name,

            "content": json.dumps(result),
        })


    final_response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=messages,

    )



    print("\n========================================")

    print("FINAL RESPONSE:")

    print("========================================")

    print(
        final_response
        .choices[0]
        .message
        .content
    )


else:

    print("\nLLM answered without using a tool:")

    print(assistant_message.content)