from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    HOUSE = os.getenv("HOUSE")
    API_HOST = os.getenv("API_HOST")
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
    RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
    RABBITMQ_QUEUE_PREFIX = os.getenv("RABBITMQ_QUEUE_PREFIX")
    RABBITMQ_QUEUE = f"{RABBITMQ_QUEUE_PREFIX}_house_{HOUSE}"
    TAPO_USERNAME = os.getenv("TAPO_USERNAME")
    TAPO_PASSWORD = os.getenv("TAPO_PASSWORD")