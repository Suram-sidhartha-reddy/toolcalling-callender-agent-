from app.tools.calendar import (
    create_event,
    list_events,
    update_event,
    delete_event,
)


# CREATE
created = create_event.invoke({
    "title": "CRUD Test",
    "date": "2026-09-23",
    "time": "19:00",
})

print("\nCREATE:")
print(created)

event_id = created["event"]["id"]


# UPDATE
updated = update_event.invoke({
    "event_id": event_id,
    "title": "Updated CRUD Test",
    "time": "20:00",
})

print("\nUPDATE:")
print(updated)


# LIST
listed = list_events.invoke({
    "date": "2026-09-23",
})

print("\nLIST:")
print(listed)


# DELETE
deleted = delete_event.invoke({
    "event_id": event_id,
})

print("\nDELETE:")
print(deleted)