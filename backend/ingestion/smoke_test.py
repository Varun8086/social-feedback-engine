from datetime import datetime, timezone
from backend.ingestion.db import get_conn
from backend.ingestion.models import RawPost
from backend.ingestion.repository import get_or_create_source, insert_posts

post = RawPost("youtube", "vid1", "c1", "hello world",
               datetime.now(timezone.utc), author="me")

with get_conn() as conn:
    sid = get_or_create_source(conn, "youtube", "vid1")
    print("first run:", insert_posts(conn, sid, [post]))
    print("second run:", insert_posts(conn, sid, [post]))
    conn.rollback()  # undo everything, so no fake data is left in the DB