from config import Config
from tapo_controller import TapoController
import aio_pika
import requests
import asyncio
import logging
import re

class RabbitListener:
    def __init__(self):
        self.tapo_controller = TapoController()
        self.bulbs = []

        self.fetch_bulbs()

    def fetch_bulbs(self):
        logging.info("Fetching bulbs from API...")

        try:
            self.bulbs = requests.get(f"http://{Config.API_HOST}/api/bulbs?house={Config.HOUSE}").json()["bulbs"]
        except Exception as error:
            logging.error(error)

    async def start_listening(self):
        # Create a connection to all bulbs so they can update instantly.
        await self.tapo_controller.initialize_bulbs(self.bulbs)
        
        # Create the RabbitMQ connection.
        connection = await aio_pika.connect_robust(
            host = Config.RABBITMQ_HOST,
            login = Config.RABBITMQ_USERNAME,
            password = Config.RABBITMQ_PASSWORD
        )
        channel = await connection.channel()
        queue = await channel.declare_queue(name = Config.RABBITMQ_QUEUE)

        logging.info(f"Listening for messages in the '{Config.RABBITMQ_QUEUE}' RabbitMQ queue.")

        # Consume messages in the RabbitMQ queue for the lifetime of the application.
        await queue.consume(self.callback)
        await asyncio.Future()

    async def callback(self, message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                message_body = json.loads(message.body.decode())
                
                id = message_body["id"]
                state = message_body["state"]
                brightness = message_body["brightness"]
                color = message_body["color"]

                # Validate that id is a number.
                if not isinstance(id, int):
                    raise ValueError(f"Invalid id: {id} - id must be a number.")
                
                # Validate that bulb is in configuration.
                if not any(bulb["id"] == id for bulb in self.bulbs):
                    raise ValueError(f"Invalid bulb: {id} - bulb not found in configuration.")

                # Validate that state is "on" or "off".
                if state not in ["on", "off"]:
                    raise ValueError(f"Invalid state: {state} - must be 'on' or 'off'.")

                # Validate that brightness is a number between 1 and 100.
                if not isinstance(brightness, int) or not (1 <= brightness <= 100):
                    raise ValueError(f"Invalid brightness: {brightness} - must be a number between 1 and 100.")
                
                # Validate that color is a hex color code.
                if not re.match(r"^#?([A-Fa-f0-9]{6})$", color):
                    raise ValueError(f"Invalid color: {color} - must be a hex color code.")

                # Control the bulb asynchronously.
                await self.tapo_controller.control_bulb(id, state, brightness, color)
            except Exception as error:
                logging.error(error)