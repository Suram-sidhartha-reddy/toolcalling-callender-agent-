import os

from dotenv import load_dotenv


load_dotenv()


API_BASE_URL = os.getenv(
    "CALENDAR_AGENT_API_URL",
    "http://127.0.0.1:8000",
)

API_TIMEOUT = float(
    os.getenv(
        "CALENDAR_AGENT_API_TIMEOUT",
        "30",
    )
)