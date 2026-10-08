class DomainError(Exception):
    """Base exception for application business-rule violations."""


class InvalidMessageError(DomainError):
    """Raised when a message violates domain rules."""


class MissingSenderError(DomainError):
    """Raised when an incoming message has no sender."""


class ConversationNotFoundError(DomainError):
    """Raised when a conversation is unavailable to the user."""