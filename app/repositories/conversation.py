import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Conversation
from app.domain.exceptions import ConversationNotFoundError


class ConversationRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_for_user(
        self,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Conversation:
        conversation = self.db.scalar(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
        )

        if conversation is None:
            raise ConversationNotFoundError(
                "Conversation not found."
            )

        return conversation

    def create(
        self,
        user_id: uuid.UUID,
    ) -> Conversation:
        conversation = Conversation(
            user_id=user_id,
        )

        self.db.add(conversation)
        self.db.flush()

        return conversation