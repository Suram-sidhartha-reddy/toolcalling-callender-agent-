import uuid
from collections.abc import Callable

from sqlalchemy.orm import Session

from app.agent import run_agent
from app.domain.policies import validate_chat_request
from app.repositories.conversation import ConversationRepository
from app.repositories.message import MessageRepository
from app.schemas.chat import ChatRequest, ChatResponse


class ChatService:

    def __init__(
        self,
        db: Session,
        agent_runner: Callable = run_agent,
    ):
        self.db = db
        self.agent_runner = agent_runner

        self.conversations = ConversationRepository(db)
        self.messages = MessageRepository(db)

    def process_chat(
        self,
        request: ChatRequest,
        request_id: str,
        user_id: uuid.UUID,
    ) -> ChatResponse:

        message = request.message.strip()

        validate_chat_request(
            message=message,
            source=request.source,
            sender=request.sender,
        )

        # ---------------------------------------
        # 1. Find/create conversation
        # ---------------------------------------

        if request.conversation_id:

            conversation = self.conversations.get_for_user(
                conversation_id=request.conversation_id,
                user_id=user_id,
            )

        else:

            conversation = self.conversations.create(
                user_id=user_id,
            )

        # ---------------------------------------
        # 2. Load previous history
        # ---------------------------------------

        previous_messages = (
            self.messages.list_history(
                conversation_id=conversation.id,
                limit=50,
            )
        )

        history = [
            {
                "role": item.role,
                "content": item.content,
            }
            for item in previous_messages
            if item.role in {"user", "assistant"}
        ]

        # ---------------------------------------
        # 3. Persist current user message
        # ---------------------------------------

        self.messages.add(
            conversation_id=conversation.id,
            role="user",
            content=message,
        )

        self.db.commit()

        # ---------------------------------------
        # 4. Run agent with history
        # ---------------------------------------

        response = self.agent_runner(
            user_message=message,
            source=request.source,
            sender=request.sender,
            history=history,
        )

        # ---------------------------------------
        # 5. Persist assistant response
        # ---------------------------------------

        self.messages.add(
            conversation_id=conversation.id,
            role="assistant",
            content=response,
        )

        self.db.commit()

        return ChatResponse(
            response=response,
            request_id=request_id,
            conversation_id=conversation.id,
        )