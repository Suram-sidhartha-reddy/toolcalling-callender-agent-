from app.tools.calendar import (
    create_event,
    list_events,
    update_event,
    delete_event,
)


# ==========================================
# 1. CREATE
# ==========================================

result = create_event(
    title="Meeting with Rahul",
    date="2026-09-23",
    time="16:00"
)

print("\nCREATE RESULT:")
print(result)


# Get the event ID
event_id = result["event"]["id"]


# ==========================================
# 2. LIST
# ==========================================

result = list_events()

print("\nLIST RESULT:")
print(result)


# ==========================================
# 3. UPDATE
# ==========================================

result = update_event(
    event_id=event_id,
    time="17:00"
)

print("\nUPDATE RESULT:")
print(result)


# ==========================================
# 4. LIST AGAIN
# ==========================================

result = list_events()

print("\nLIST AFTER UPDATE:")
print(result)


# ==========================================
# 5. DELETE
# ==========================================

result = delete_event(
    event_id=event_id
)

print("\nDELETE RESULT:")
print(result)


# ==========================================
# 6. LIST AGAIN
# ==========================================

result = list_events()

print("\nFINAL LIST:")
print(result)