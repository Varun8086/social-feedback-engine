from collections import defaultdict

from backend.ingestion.db import get_conn
from backend.ingestion.repository import (
    get_or_create_source, insert_posts, start_run, finish_run,
)


def ingest(platform, posts):
    grouped = defaultdict(list)
    for p in posts:
        grouped[p.source_external_id].append(p)

    total = 0
    with get_conn() as conn:
        for ext_id, batch in grouped.items():
            sid = get_or_create_source(conn, platform, ext_id)
            run_id = start_run(conn, sid)
            conn.commit()
            try:
                n = insert_posts(conn, sid, batch)
                finish_run(conn, run_id, "success", len(batch), n)
                total += n
            except Exception as e:
                conn.rollback()
                finish_run(conn, run_id, "failed", len(batch), 0, str(e))
                conn.commit()
                raise
            conn.commit()
    return total