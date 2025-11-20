import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core import otel_logs

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger("background-main")
otel_logs.init_logging()


async def main():
    """
    The main coroutine that sets up the scheduler and runs the application's event loop.
    """
    scheduler = AsyncIOScheduler()

    ## ADD A FUNC/METHOD TO RUN PERIODICALLY
    scheduler.add_job("", "interval", minutes=1)

    scheduler.start()
    logger.info("APScheduler service started. Press Ctrl+C to exit.")

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler shut down gracefully.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Async cron service stopped.")
