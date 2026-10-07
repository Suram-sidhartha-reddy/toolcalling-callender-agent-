from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Message sent to the calendar agent",
    )

    source: str = Field(
        default="user_command",
        description="Origin of the message",
    )

    sender: str | None = Field(
        default=None,
        max_length=255,
        description="Sender identifier for incoming messages",
    )


class ChatResponse(BaseModel):
    response: str
    request_id: str