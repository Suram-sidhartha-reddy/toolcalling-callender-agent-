from app.integrations.google_calendar import get_calendar_service


service = get_calendar_service()

events = service.events().list(
    calendarId="primary",
    maxResults=10,
    singleEvents=True,
    orderBy="startTime"
).execute()

print("Google Calendar connected successfully!")

items = events.get("items", [])

if not items:
    print("No events found.")
else:
    print("\nUpcoming events:")

    for event in items:
        start = event["start"].get(
            "dateTime",
            event["start"].get("date")
        )

        print(f"- {start} | {event.get('summary', '(No title)')}")