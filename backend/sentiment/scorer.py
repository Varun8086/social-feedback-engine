import sys

from backend.ingestion.db import get_conn
from backend.sentiment.model import MODEL, score_texts

BATCH = 64

SELECT_SQL = """
    SELECT id, body FROM posts
    WHERE sentiment_label IS NULL
    ORDER BY id LIMIT %s
    FOR UPDATE SKIP LOCKED
"""
UPDATE_SQL = """
    UPDATE posts
    SET sentiment_label = %s, sentiment_score = %s,
        sentiment_model = %s, scored_at = now()
    WHERE id = %s
"""


def build_updates(rows, results):
    """Pair each (id, body) row with its (label, score) result."""
    return [
        (label, float(score), MODEL, post_id)
        for (post_id, _body), (label, score) in zip(rows, results)
    ]


def score_pending(limit=None):
    total = 0
    with get_conn() as conn:
        while limit is None or total < limit:
            rows = conn.execute(SELECT_SQL, (BATCH,)).fetchall()
            if not rows:
                break
            results = score_texts([body for _id, body in rows])
            conn.cursor().executemany(UPDATE_SQL, build_updates(rows, results))
            conn.commit()  # save each batch, so a crash loses at most one
            total += len(rows)
            print(f"scored {total}")
    return total


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    print(f"done, scored {score_pending(limit)} posts")