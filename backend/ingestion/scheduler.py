import logging
import os

from apscheduler.schedulers.blocking import BlockingScheduler

from backend.ingestion.db import get_conn
from backend.ingestion.run_all import run_all

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")


def ran_recently(hours=20) -> bool:
    with get_conn() as conn:
        n = conn.execute(
            "SELECT count(*) FROM ingestion_runs "
            "WHERE started_at > now() - make_interval(hours => %s)",
            (hours,),
        ).fetchone()[0]
    return n > 0


if __name__ == "__main__":
    hour = int(os.getenv("RUN_HOUR_UTC", "2"))
    minute = int(os.getenv("RUN_MINUTE_UTC", "0"))

    if not ran_recently():
        logging.info("no run in the last 20h; catching up now")
        run_all()

    sched = BlockingScheduler(timezone="UTC")
    sched.add_job(run_all, "cron", hour=hour, minute=minute,
                  misfire_grace_time=6 * 3600, coalesce=True)
    logging.info("scheduler started; daily run at %02d:%02d UTC", hour, minute)
    sched.start()