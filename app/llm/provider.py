
import os
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

load_dotenv()


class MockLLM:
    """Offline LLM substitute for development and tests."""

    def invoke(self, messages: list[Any]) -> AIMessage:
        user_messages = []

        for message in messages:
            if isinstance(message, dict):
                if message.get("role") == "user":
                    user_messages.append(message.get("content", ""))

            elif getattr(message, "type", None) == "human":
                user_messages.append(
                    getattr(message, "content", "")
                )

        latest = user_messages[-1] if user_messages else ""

        return AIMessage(
            content=f"[MOCK MODE] Received your message: {latest}"
        )


def create_llm():
    provider = os.getenv("LLM_PROVIDER", "mock").lower()

    if provider == "mock":
        return MockLLM(), False

    if provider == "huggingface":
        api_key = os.getenv("HF_TOKEN")

        if not api_key:
            raise ValueError("HF_TOKEN is not configured.")

        model = os.getenv(
            "LLM_MODEL",
            "openai/gpt-oss-120b",
        )
        base_url = os.getenv(
            "LLM_BASE_URL",
            "https://router.huggingface.co/v1",
        )

    elif provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not configured.")

        model = os.getenv(
            "LLM_MODEL",
            "openai/gpt-oss-120b",
        )
        base_url = os.getenv(
            "LLM_BASE_URL",
            "https://api.groq.com/openai/v1",
        )

    else:
        raise ValueError(
            f"Unsupported LLM_PROVIDER: {provider}"
        )

    llm = ChatOpenAI(
        model=model,
        base_url=base_url,
        api_key=api_key,
    )

    # Keep function/tool calling enabled for the agent.
    return llm, True
