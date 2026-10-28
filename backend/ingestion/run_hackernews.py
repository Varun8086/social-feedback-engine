from dotenv import load_dotenv
load_dotenv()

from backend.ingestion.pipeline import ingest
from backend.ingestion.sources.hackernews import HackerNewsSource

from backend.ingestion.config import KEYWORDS


def main():
    posts = HackerNewsSource(KEYWORDS).fetch()
    inserted = ingest("hackernews", posts)
    print(f"fetched {len(posts)}, inserted {inserted}")


if __name__ == "__main__":
    main()