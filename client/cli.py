import argparse

from client.api_client import APIError, CalendarAPIClient


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calendar AI Agent CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # -------------------------------------------------
    # health command
    # -------------------------------------------------

    subparsers.add_parser(
        "health",
        help="Check whether the API is running",
    )

    # -------------------------------------------------
    # chat command
    # -------------------------------------------------

    chat_parser = subparsers.add_parser(
        "chat",
        help="Chat with the Calendar AI Agent",
    )

    # Optional positional message.
    #
    # This allows BOTH:
    #
    # python -m client.cli chat
    #
    # and:
    #
    # python -m client.cli chat "What do I have tomorrow?"
    #
    chat_parser.add_argument(
        "message",
        nargs="?",
        help="Message to send to the agent",
    )

    chat_parser.add_argument(
        "--source",
        default="user_command",
        choices=[
            "user_command",
            "incoming_message",
        ],
        help="Source of the message",
    )

    chat_parser.add_argument(
        "--sender",
        default=None,
        help="Sender identifier for incoming messages",
    )

    chat_parser.add_argument(
        "--conversation-id",
        default=None,
        help="Continue an existing conversation",
    )

    return parser


def interactive_chat(
    client: CalendarAPIClient,
    conversation_id: str | None = None,
    source: str = "user_command",
    sender: str | None = None,
) -> None:
    """
    Run an interactive multi-turn chat session.

    The conversation_id returned by the API is reused for
    every subsequent message so the server can restore
    the same conversation.
    """

    print()
    print("======================================")
    print("       Calendar AI Agent")
    print("======================================")
    print("Type /exit or /quit to leave.")
    print()

    while True:

        try:
            message = input("You: ").strip()

        except (KeyboardInterrupt, EOFError):
            print()
            print("Exiting...")
            break

        # Exit commands
        if message.lower() in {"/exit", "/quit"}:
            print("Goodbye!")
            break

        # Ignore empty messages
        if not message:
            continue

        try:
            result = client.chat(
                message=message,
                source=source,
                sender=sender,
                conversation_id=conversation_id,
            )

            # Save the conversation ID returned by the server.
            #
            # First message:
            #     conversation_id = None
            #
            # Server creates one.
            #
            # Next messages:
            #     same conversation_id is sent back.
            new_conversation_id = result["conversation_id"]

            if conversation_id is None:
                conversation_id = new_conversation_id
                print()
                print(f"Conversation ID: {conversation_id}")

            print()
            print("Agent:")
            print(result["response"])
            print()

        except APIError as exc:
            print()
            print(f"API Error: {exc}")
            print()


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    client = CalendarAPIClient()

    try:

        # -------------------------------------------------
        # HEALTH
        # -------------------------------------------------

        if args.command == "health":

            result = client.health_check()

            print(result["message"])

            return

        # -------------------------------------------------
        # CHAT
        # -------------------------------------------------

        if args.command == "chat":

            # ---------------------------------------------
            # Interactive mode
            # ---------------------------------------------
            #
            # python -m client.cli chat
            #
            if args.message is None:

                interactive_chat(
                    client=client,
                    conversation_id=args.conversation_id,
                    source=args.source,
                    sender=args.sender,
                )

                return

            # ---------------------------------------------
            # Single-message mode
            # ---------------------------------------------
            #
            # python -m client.cli chat "Hello"
            #

            result = client.chat(
                message=args.message,
                source=args.source,
                sender=args.sender,
                conversation_id=args.conversation_id,
            )

            print()
            print("Agent:")
            print(result["response"])
            print()

            print(
                f"Conversation ID: "
                f"{result['conversation_id']}"
            )

            return

    except APIError as exc:

        print(f"API Error: {exc}")

        raise SystemExit(1)


if __name__ == "__main__":
    main()