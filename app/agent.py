import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from langgraph.graph import (
    MessagesState,
    StateGraph,
    START,
    END,
)

from langgraph.prebuilt import (
    ToolNode,
    tools_condition,
)

from app.tools.registry import TOOLS


load_dotenv()


hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise ValueError(
        "HF_TOKEN not found in .env"
    )


llm = ChatOpenAI(
    model="openai/gpt-oss-120b",
    base_url="https://router.huggingface.co/v1",
    api_key=hf_token,
)


llm_with_tools = llm.bind_tools(TOOLS)


def call_llm(state):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


tool_node = ToolNode(TOOLS)


graph = StateGraph(MessagesState)


graph.add_node(
    "llm",
    call_llm
)

graph.add_node(
    "tools",
    tool_node
)


graph.add_edge(
    START,
    "llm"
)


graph.add_conditional_edges(
    "llm",
    tools_condition,
)


graph.add_edge(
    "tools",
    "llm"
)


app = graph.compile()
def run_agent(user_message: str) -> str:
    result = app.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_message,
            }
        ]
    })

    return result["messages"][-1].content