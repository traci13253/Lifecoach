"""Celery-based worker for sending session reminders."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from celery import Celery

# Configuration for Celery. In a production application the broker URL would
# come from configuration or environment variables. Here we default to a local
# Redis instance to keep the example simple.
app = Celery("reminders", broker="redis://localhost:6379/0")


@app.task
def send_email_reminder(session_id: str, email: str, when: Optional[datetime] = None) -> str:
    """Send an email reminder for a session.

    In a real system this would integrate with an email provider. For this
    project we simply return a message so the task can be tested easily.
    """
    when_str = when.isoformat() if when else "immediately"
    return f"Reminder for session {session_id} to {email} scheduled {when_str}"
