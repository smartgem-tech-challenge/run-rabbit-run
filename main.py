from rabbit_listener import RabbitListener
import asyncio
import logging
import sys

async def main():
    listener = RabbitListener()
    await listener.start_listening()

if __name__ == "__main__":
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
    )

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Shutting down...")
        sys.exit(0)
    except Exception as error:
        logging.error(error)
        sys.exit(1)