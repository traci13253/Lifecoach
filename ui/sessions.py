"""Simple interface helpers for viewing sessions and creating reminders."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterable

from backend.calendar import Session
from worker.reminders import send_email_reminder


def format_session(session: Session) -> str:
    """Return a human readable representation of a session."""
    start = session.start.strftime("%Y-%m-%d %H:%M")
    end = session.end.strftime("%Y-%m-%d %H:%M")
    return f"{session.summary} ({start} - {end})"


def list_upcoming_sessions(sessions: Iterable[Session]) -> list[str]:
    """Return formatted strings for a list of sessions."""
    return [format_session(s) for s in sessions]


def set_reminder(session: Session, email: str, minutes_before: int = 10) -> str:
    """Schedule a reminder email using the Celery worker."""
    reminder_time = session.start - timedelta(minutes=minutes_before)
    return send_email_reminder.apply_async(
        (session.summary, email, reminder_time), eta=reminder_time
    ).id
