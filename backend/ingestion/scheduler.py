import logging
import os

from apscheduler.schedulers.blocking import BlockingScheduler

from backend.ingestion.run_all import run_all

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

if __name__ == "__main__":
    hour = int(os.getenv("RUN_HOUR_UTC", "2"))
    minute = int(os.getenv("RUN_MINUTE_UTC", "0"))
    sched = BlockingScheduler(timezone="UTC")
    sched.add_job(run_all, "cron", hour=hour, minute=minute)
    logging.info("scheduler started; daily run at %02d:%02d UTC", hour, minute)
    sched.start()