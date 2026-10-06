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

    # -----------------------------
    # health
    # -----------------------------
    subparsers.add_parser(
        "health",
        help="Check whether the API is running",
    )

    # -----------------------------
    # chat
    # -----------------------------
    chat_parser = subparsers.add_parser(
        "chat",
        help="Chat with the Calendar AI Agent",
    )

    # nargs="?" makes message optional
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
    )

    chat_parser.add_argument(
        "--sender",
        default=None,
        help="Sender identifier for incoming messages",
    )

    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    client = CalendarAPIClient()

    try:

        if args.command == "health":
            result = client.health_check()
            print(result["message"])
            return

        if args.command == "chat":

            message = args.message

            # Interactive mode
            if not message:
                message = input("Enter your message: ")

            # Prevent empty messages
            if not message.strip():
                print("Message cannot be empty.")
                return

            result = client.chat(
                message=message,
                source=args.source,
                sender=args.sender,
            )

            print()
            print("Agent:")
            print(result["response"])
            return

    except APIError as exc:
        print(f"API Error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()