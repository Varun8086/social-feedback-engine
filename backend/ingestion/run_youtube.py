from dotenv import load_dotenv
load_dotenv()

from backend.ingestion.config import KEYWORDS, MIN_VIEWS
from backend.ingestion.pipeline import ingest
from backend.ingestion.sources.youtube import YouTubeSource


def main():
    source = YouTubeSource([])
    ids = source.discover(KEYWORDS, MIN_VIEWS)
    print(f"discovered {len(ids)} videos with >= {MIN_VIEWS} views")
    posts = source.fetch()
    inserted = ingest("youtube", posts)
    print(f"fetched {len(posts)}, inserted {inserted}")


if __name__ == "__main__":
    main()