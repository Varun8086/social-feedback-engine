def get_or_create_source(conn, platform, external_id) -> int:
    row = conn.execute(
        """INSERT INTO sources (platform, external_id) VALUES (%s, %s)
           ON CONFLICT (platform, external_id)
           DO UPDATE SET platform = EXCLUDED.platform
           RETURNING id""",
        (platform, external_id),
    ).fetchone()
    return row[0]

def insert_posts(conn, source_id, posts) -> int:
    inserted = 0
    for p in posts:
        cur = conn.execute(
            """INSERT INTO posts
               (source_id, external_id, author, title, body, url, score, posted_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (source_id, external_id) DO NOTHING""",
            (source_id, p.external_id, p.author, p.title,
             p.body, p.url, p.score, p.posted_at),
        )
        inserted += cur.rowcount  # 1 if inserted, 0 if skipped
    return inserted

def start_run(conn, source_id) -> int:
    return conn.execute(
        "INSERT INTO ingestion_runs (source_id) VALUES (%s) RETURNING id",
        (source_id,),
    ).fetchone()[0]

def finish_run(conn, run_id, status, fetched, inserted, error=None):
    conn.execute(
        """UPDATE ingestion_runs
           SET finished_at = now(), status = %s,
               posts_fetched = %s, posts_inserted = %s, error = %s
           WHERE id = %s""",
        (status, fetched, inserted, error, run_id),
    )