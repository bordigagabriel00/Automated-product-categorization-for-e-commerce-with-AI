import logging
from nats.aio.client import Client as NATS
import config

topic_predict_request = "predict.request"
topic_predict_response = "predict.response"
topic_health = "health"


class NatsProvider:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NatsProvider, cls).__new__(cls)
            # Only once
            cls._instance.nc = NATS()
            cls._instance.is_connected = False
        return cls._instance

    def __init__(self, servers=None, max_reconnect_attempts=5, reconnect_time_wait=2):
        self.is_connected = None
        if servers is None:
            servers = ["nats://127.0.0.1:4222"]
        self.servers = servers
        self.max_reconnect_attempts = max_reconnect_attempts
        self.reconnect_time_wait = reconnect_time_wait

    async def connect(self):
        if not self.is_connected:
            options = {
                "servers": self.servers,
                "max_reconnect_attempts": self.max_reconnect_attempts,
                "reconnect_time_wait": self.reconnect_time_wait,
            }
            try:
                await self.nc.connect(**options)
                self.is_connected = True
                logging.info("Connected to NATS")
            except Exception as e:
                logging.error(f"Failed to connect to NATS: {e}")
                raise

    async def publish(self, subject, message):
        await self.connect()
        try:
            await self.nc.publish(subject, message.encode())
            logging.info(f"Published message to {subject}")
        except Exception as e:
            logging.error(f"Failed to publish message: {e}")
            raise

    async def subscribe(self, subject, callback):
        await self.connect()
        try:
            await self.nc.subscribe(subject, cb=callback)
            logging.info(f"Subscribed to {subject}")
        except Exception as e:
            logging.error(f"Failed to subscribe: {e}")
            raise

    async def close(self):
        try:
            await self.nc.close()
            self.is_connected = False
            logging.info("NATS connection closed")
        except Exception as e:
            logging.error(f"Failed to close NATS connection: {e}")
            raise


# Uso del objeto global
nats_provider = NatsProvider([config.settings.nats_url])
