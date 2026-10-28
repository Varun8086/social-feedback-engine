import logging

from dotenv import load_dotenv
load_dotenv()

from backend.ingestion import run_hackernews, run_youtube

log = logging.getLogger(__name__)


def run_all():
    for name, job in [("youtube", run_youtube.main),
                      ("hackernews", run_hackernews.main)]:
        try:
            job()
        except Exception:
            log.exception("%s ingestion failed", name)  # keep going


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_all()