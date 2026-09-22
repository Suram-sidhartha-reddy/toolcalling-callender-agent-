import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from app.tools.registry import (
    TOOLS,
    TOOL_FUNCTIONS,
)



load_dotenv()

hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise ValueError(
        "HF_TOKEN not found in .env"
    )




client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_token,
)



messages = [

    {
        "role": "system",
        "content": (
            "You are a calendar assistant. "
            "Use the available calendar tools "
            "when the user requests calendar actions."
        ),
    },

    {
        "role": "user",
        "content": (
            "let me know when can i meet u "
            
        ),
    },
]



response = client.chat.completions.create(

    model="openai/gpt-oss-120b",

    messages=messages,

    tools=TOOLS,

    tool_choice="auto",
)


assistant_message = response.choices[0].message



if not assistant_message.tool_calls:

    print("\nLLM RESPONSE:")
    print(assistant_message.content)

    raise SystemExit




messages.append(assistant_message)



for tool_call in assistant_message.tool_calls:

    function_name = tool_call.function.name

    arguments = json.loads(
        tool_call.function.arguments
    )

    print("\n================================")
    print("TOOL CALL")
    print("================================")

    print("Tool:")
    print(function_name)

    print("\nArguments:")
    print(arguments)



    function = TOOL_FUNCTIONS.get(
        function_name
    )


    if function is None:

        result = {
            "success": False,
            "error": (
                f"Unknown tool: {function_name}"
            ),
        }

    else:

        try:

            result = function(
                **arguments
            )

        except Exception as e:

            result = {
                "success": False,
                "error": str(e),
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




print("\n================================")
print("FINAL RESPONSE")
print("================================")

print(
    final_response
    .choices[0]
    .message
    .content
)