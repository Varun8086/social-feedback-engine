from dotenv import load_dotenv
load_dotenv()

from backend.ingestion.pipeline import ingest
from backend.ingestion.sources.youtube import YouTubeSource

VIDEO_IDS = ["ecmbMYIzNLs", "KhnVcAC5bIM"]


def main():
    posts = YouTubeSource(VIDEO_IDS).fetch()
    inserted = ingest("youtube", posts)
    print(f"fetched {len(posts)}, inserted {inserted}")


if __name__ == "__main__":
    main()