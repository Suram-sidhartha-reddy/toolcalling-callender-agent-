from typing import Optional

from langchain_core.tools import tool

from app.integrations.google_calendar import get_calendar_service
from datetime import datetime

def normalize_time(time_str: str) -> str:
    """Convert common time formats to HH:MM."""

    formats = [
        "%H:%M",
        "%H:%M:%S",
        "%I:%M %p",
        "%I %p",
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(time_str.strip(), fmt)
            return parsed.strftime("%H:%M")
        except ValueError:
            continue

    raise ValueError(
        f"Invalid time format: {time_str}. "
        "Expected formats such as 18:00 or 6:00 PM."
    )
@tool
def create_event(title: str, date: str, time: str):
    """Create a new event in the user's Google Calendar."""

    print("\n========== CREATE EVENT TOOL ==========")
    print("TITLE:", title)
    print("DATE:", date)
    print("TIME FROM LLM:", time)

    normalized_time = normalize_time(time)

    print("NORMALIZED TIME:", normalized_time)

    service = get_calendar_service()

    event = {
        "summary": title,
        "start": {
            "dateTime": f"{date}T{normalized_time}:00",
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": f"{date}T{normalized_time}:00",
            "timeZone": "Asia/Kolkata",
        },
    }

    print("GOOGLE EVENT BODY:")
    print(event)

    created_event = service.events().insert(
        calendarId="primary",
        body=event,
    ).execute()

    return {
        "success": True,
        "event": {
            "id": created_event["id"],
            "title": created_event.get("summary"),
            "start": created_event["start"].get("dateTime"),
            "link": created_event.get("htmlLink"),
        },
    }


@tool
def list_events(date: Optional[str] = None):
    """List events from the user's Google Calendar."""

    service = get_calendar_service()

    params = {
        "calendarId": "primary",
        "singleEvents": True,
        "orderBy": "startTime",
    }

    if date:
        params["timeMin"] = f"{date}T00:00:00+05:30"
        params["timeMax"] = f"{date}T23:59:59+05:30"

    result = service.events().list(**params).execute()

    events = []

    for event in result.get("items", []):
        events.append({
            "id": event["id"],
            "title": event.get("summary", "(No title)"),
            "start": event["start"].get(
                "dateTime",
                event["start"].get("date")
            ),
            "link": event.get("htmlLink"),
        })

    return {
        "success": True,
        "events": events,
    }

@tool
def update_event(
    event_id: str,
    title: Optional[str] = None,
    date: Optional[str] = None,
    time: Optional[str] = None,
):
    """Update an existing Google Calendar event."""

    service = get_calendar_service()

    # Get the existing event
    existing_event = service.events().get(
        calendarId="primary",
        eventId=event_id,
    ).execute()

    if title is not None:
        existing_event["summary"] = title

    # For this learning project, handle timed events.
    if date is not None or time is not None:

        current_start = existing_event["start"].get("dateTime")

        if current_start:
            current_date = current_start[:10]
            current_time = current_start[11:16]
        else:
            current_date = date
            current_time = time

        new_date = date or current_date
        new_time = time or current_time

        start_datetime = f"{new_date}T{new_time}:00"

        existing_event["start"] = {
            "dateTime": start_datetime,
            "timeZone": "Asia/Kolkata",
        }

        existing_event["end"] = {
            "dateTime": start_datetime,
            "timeZone": "Asia/Kolkata",
        }

    updated_event = service.events().update(
        calendarId="primary",
        eventId=event_id,
        body=existing_event,
    ).execute()

    return {
        "success": True,
        "event": {
            "id": updated_event["id"],
            "title": updated_event.get("summary"),
            "start": updated_event["start"].get(
                "dateTime",
                updated_event["start"].get("date")
            ),
            "link": updated_event.get("htmlLink"),
        },
    }

@tool
def delete_event(event_id: str):
    """Delete an existing Google Calendar event."""

    service = get_calendar_service()

    try:
        service.events().delete(
            calendarId="primary",
            eventId=event_id,
        ).execute()

        return {
            "success": True,
            "deleted_event_id": event_id,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }





@tool
def find_free_slots(
    date: str,
    start_hour: int = 9,
    end_hour: int = 18,
):
    """
    Find available one-hour time slots in the user's Google Calendar
    for a specific date.

    date must be in YYYY-MM-DD format.
    start_hour and end_hour define the working-hour window.
    """

    service = get_calendar_service()

    params = {
        "calendarId": "primary",
        "timeMin": f"{date}T00:00:00+05:30",
        "timeMax": f"{date}T23:59:59+05:30",
        "singleEvents": True,
        "orderBy": "startTime",
    }

    result = service.events().list(**params).execute()

    events = result.get("items", [])

    busy_hours = set()

    for event in events:
        start = event.get("start", {}).get("dateTime")

        if not start:
            continue

        # Extract hour from:
        # 2026-09-24T14:00:00+05:30
        event_time = datetime.fromisoformat(start)

        busy_hours.add(event_time.hour)

    free_slots = []

    for hour in range(start_hour, end_hour):
        if hour not in busy_hours:
            start_time = f"{hour:02d}:00"
            end_time = f"{hour + 1:02d}:00"

            free_slots.append({
                "start": start_time,
                "end": end_time,
            })

    return {
        "success": True,
        "date": date,
        "free_slots": free_slots,
    }