from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
    )

    source: Literal[
        "user_command",
        "incoming_message",
    ] = "user_command"

    sender: str | None = Field(
        default=None,
        max_length=255,
    )


class ChatResponse(BaseModel):
    response: str
    request_id: str