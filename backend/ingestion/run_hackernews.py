from dotenv import load_dotenv
load_dotenv()

from backend.ingestion.pipeline import ingest
from backend.ingestion.sources.hackernews import HackerNewsSource

QUERIES = ["claude code", "cursor ai"]


def main():
    posts = HackerNewsSource(QUERIES).fetch()
    inserted = ingest("hackernews", posts)
    print(f"fetched {len(posts)}, inserted {inserted}")


if __name__ == "__main__":
    main()