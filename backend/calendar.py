"""Calendar integration for scheduling sessions using Google Calendar or iCal."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
except Exception:  # pragma: no cover - library might not be installed during tests
    Credentials = None
    build = None


@dataclass
class Session:
    """Representation of a coaching session."""
    summary: str
    start: datetime
    end: datetime
    attendees: Optional[List[str]] = None


def _build_google_service(credentials: Credentials):
    """Create a Google Calendar service instance if dependencies are available."""
    if build is None:
        raise RuntimeError("google-api-python-client is not installed")
    return build("calendar", "v3", credentials=credentials)


def schedule_with_google_calendar(session: Session, credentials: Credentials, calendar_id: str = "primary"):
    """Schedule a session in Google Calendar.

    Parameters
    ----------
    session:
        The session to schedule.
    credentials:
        OAuth credentials for the Google Calendar API.
    calendar_id:
        Calendar ID where the event will be created.
    """
    service = _build_google_service(credentials)

    event = {
        "summary": session.summary,
        "start": {"dateTime": session.start.isoformat()},
        "end": {"dateTime": session.end.isoformat()},
    }
    if session.attendees:
        event["attendees"] = [{"email": email} for email in session.attendees]

    return service.events().insert(calendarId=calendar_id, body=event).execute()


def schedule_with_ical(session: Session, file_path: str) -> None:
    """Create an iCal file with a single session event.

    This is a very small substitute for full iCal integration and is
    sufficient for demo and testing purposes.
    """
    ics_event = (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "BEGIN:VEVENT\n"
        f"SUMMARY:{session.summary}\n"
        f"DTSTART:{session.start.strftime('%Y%m%dT%H%M%S')}\n"
        f"DTEND:{session.end.strftime('%Y%m%dT%H%M%S')}\n"
        "END:VEVENT\n"
        "END:VCALENDAR\n"
    )
    with open(file_path, "w", encoding="utf-8") as fh:
        fh.write(ics_event)
