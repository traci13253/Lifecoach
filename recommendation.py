from collections import Counter
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name('analytics.db')


def recommend(user_id: str):
    """Recommend interactions with positive outcomes from similar users."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Interactions performed by the target user
    cur.execute("SELECT interaction FROM analytics WHERE user_id = ?", (user_id,))
    user_interactions = [row[0] for row in cur.fetchall()]
    if not user_interactions:
        conn.close()
        return []

    # Users who performed the same interactions
    placeholders = ",".join("?" for _ in user_interactions)
    cur.execute(
        f"SELECT user_id FROM analytics WHERE interaction IN ({placeholders}) AND user_id != ?",
        (*user_interactions, user_id),
    )
    similar_users = [row[0] for row in cur.fetchall()]
    if not similar_users:
        conn.close()
        return []

    # Positive interactions by similar users not yet tried by current user
    placeholders = ",".join("?" for _ in similar_users)
    cur.execute(
        f"""
        SELECT interaction FROM analytics
        WHERE user_id IN ({placeholders}) AND outcome = 'positive'
        """,
        similar_users,
    )
    recommendations = [row[0] for row in cur.fetchall() if row[0] not in user_interactions]
    conn.close()

    counts = Counter(recommendations)
    return [interaction for interaction, _ in counts.most_common()]
