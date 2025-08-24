import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name('analytics.db')


def init_db():
    """Create analytics table if it does not exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS analytics (
            user_id TEXT NOT NULL,
            interaction TEXT NOT NULL,
            outcome TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def log_interaction(user_id: str, interaction: str, outcome: str) -> None:
    """Store a single user interaction and outcome."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO analytics (user_id, interaction, outcome) VALUES (?, ?, ?)",
        (user_id, interaction, outcome),
    )
    conn.commit()
    conn.close()


def fetch_user_interactions(user_id: str):
    """Return list of (interaction, outcome) for a user."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT interaction, outcome FROM analytics WHERE user_id = ?", (user_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_analytics_counts():
    """Return a mapping of interaction -> number of occurrences."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT interaction, COUNT(*) FROM analytics GROUP BY interaction")
    data = {interaction: count for interaction, count in cur.fetchall()}
    conn.close()
    return data
