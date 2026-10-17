from dotenv import load_dotenv
load_dotenv()

from backend.ingestion.db import get_conn
from backend.ingestion.repository import get_or_create_source, insert_posts
from backend.ingestion.sources.youtube import YouTubeSource

VIDEO_IDS = ["ecmbMYIzNLs", "KhnVcAC5bIM"]

def main():
    posts = YouTubeSource(VIDEO_IDS).fetch()
    inserted = 0
    with get_conn() as conn:
        for vid in VIDEO_IDS:
            batch = [p for p in posts if p.source_external_id == vid]
            sid = get_or_create_source(conn, "youtube", vid)
            inserted += insert_posts(conn, sid, batch)
    print(f"fetched {len(posts)}, inserted {inserted}")

if __name__ == "__main__":
    main()