import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Message


class MessageRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(
        self,
        conversation_id: uuid.UUID,
        role: str,
        content: str,
    ) -> Message:

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.db.add(message)
        self.db.flush()

        return message

    def list_history(
        self,
        conversation_id: uuid.UUID,
        limit: int = 50,
    ) -> list[Message]:

        return list(
            self.db.scalars(
                select(Message)
                .where(
                    Message.conversation_id == conversation_id
                )
                .order_by(Message.position)
                .limit(limit)
            )
        )