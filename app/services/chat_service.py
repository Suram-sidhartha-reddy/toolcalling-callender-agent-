from collections.abc import Callable

from app.agent import run_agent
from app.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    """
    Application service for processing chat requests.

    The API layer should only deal with HTTP concerns.
    This service handles the application use case.
    """

    def __init__(
        self,
        agent_runner: Callable = run_agent,
    ):
        self.agent_runner = agent_runner

    def process_chat(
        self,
        request: ChatRequest,
        request_id: str,
    ) -> ChatResponse:

        message = request.message.strip()

        response = self.agent_runner(
            user_message=message,
            source=request.source,
            sender=request.sender,
        )

        return ChatResponse(
            response=response,
            request_id=request_id,
        )