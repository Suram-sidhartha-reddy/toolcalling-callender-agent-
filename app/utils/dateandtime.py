from datetime import datetime
from zoneinfo import ZoneInfo

APP_TIMEZONE = ZoneInfo("Asia/Kolkata")


def get_current_datetime() -> datetime:
    return datetime.now(APP_TIMEZONE)


def get_current_date() -> str:
    return get_current_datetime().date().isoformat()