from app.domain.exceptions import (
    InvalidMessageError,
    MissingSenderError,
)


VALID_SOURCES = {
    "user_command",
    "incoming_message",
}


def validate_chat_request(
    message: str,
    source: str,
    sender: str | None,
) -> None:

    message = message.strip()

    if not message:
        raise InvalidMessageError(
            "Message cannot be empty."
        )

    if source not in VALID_SOURCES:
        raise InvalidMessageError(
            f"Unsupported message source: {source}"
        )

    if source == "incoming_message":
        if not sender or not sender.strip():
            raise MissingSenderError(
                "Sender is required for incoming messages."
            )