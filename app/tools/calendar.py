from typing import Optional
import uuid


# Temporary in-memory storage
events = {}


def create_event(
    title: str,
    date: str,
    time: str
):
    """Create a new calendar event."""

    event_id = str(uuid.uuid4())

    event = {
        "id": event_id,
        "title": title,
        "date": date,
        "time": time,
    }

    events[event_id] = event

    return {
        "success": True,
        "event": event
    }


def list_events(
    date: Optional[str] = None
):
    """List calendar events, optionally filtered by date."""

    if date:
        matching_events = [
            event
            for event in events.values()
            if event["date"] == date
        ]
    else:
        matching_events = list(events.values())

    return {
        "success": True,
        "events": matching_events
    }


def update_event(
    event_id: str,
    title: Optional[str] = None,
    date: Optional[str] = None,
    time: Optional[str] = None
):
    """Update an existing event."""

    if event_id not in events:
        return {
            "success": False,
            "error": "Event not found"
        }

    event = events[event_id]

    if title is not None:
        event["title"] = title

    if date is not None:
        event["date"] = date

    if time is not None:
        event["time"] = time

    return {
        "success": True,
        "event": event
    }


def delete_event(event_id: str):
    """Delete an existing calendar event."""

    if event_id not in events:
        return {
            "success": False,
            "error": "Event not found"
        }

    deleted_event = events.pop(event_id)

    return {
        "success": True,
        "deleted_event": deleted_event
    }