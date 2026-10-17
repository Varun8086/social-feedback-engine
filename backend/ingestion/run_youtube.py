from dotenv import load_dotenv
load_dotenv()

from backend.ingestion.db import get_conn
from backend.ingestion.repository import (
    get_or_create_source, insert_posts, start_run, finish_run,
)
from backend.ingestion.sources.youtube import YouTubeSource

VIDEO_IDS = ["ecmbMYIzNLs", "KhnVcAC5bIM"]


def main():
    source = YouTubeSource(VIDEO_IDS)
    posts = source.fetch()
    inserted = 0

    with get_conn() as conn:
        for vid in source.video_ids:
            batch = [p for p in posts if p.source_external_id == vid]
            sid = get_or_create_source(conn, "youtube", vid)
            run_id = start_run(conn, sid)
            conn.commit()  # save "running" even if the next step crashes
            try:
                n = insert_posts(conn, sid, batch)
                finish_run(conn, run_id, "success", len(batch), n)
                inserted += n
            except Exception as e:
                conn.rollback()
                finish_run(conn, run_id, "failed", len(batch), 0, str(e))
                conn.commit()
                raise
            conn.commit()

    print(f"fetched {len(posts)}, inserted {inserted}")


if __name__ == "__main__":
    main()