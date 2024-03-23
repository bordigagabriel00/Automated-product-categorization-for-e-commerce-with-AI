from nats.aio.client import Client as NATS

import config
from core.logger_provider import logger
from config import settings

bert_base_prediction_request_topic = "bert.base.prediction.request"
bert_base_prediction_response_topic = "bert.base.prediction.response"

bert_ft_prediction_request_topic = "bert.ft.prediction.request"
bert_ft_prediction_response_topic = "bert.ft.prediction.response"
topic_health = "health"


class NatsProvider:
    def __init__(self, servers=None, max_reconnect_attempts=5, reconnect_time_wait=2):
        if servers is None:
            servers = [settings.nats_url]
        self.nc = NATS()
        self.servers = servers
        self.max_reconnect_attempts = max_reconnect_attempts
        self.reconnect_time_wait = reconnect_time_wait

    async def connect(self):
        options = {
            "servers": self.servers,
            "max_reconnect_attempts": self.max_reconnect_attempts,
            "reconnect_time_wait": self.reconnect_time_wait,
        }
        try:
            await self.nc.connect(**options)
            logger.info("Connected to NATS")
        except Exception as e:
            logger.error(f"Failed to connect to NATS: {e}")
            raise

    async def publish(self, subject, message):
        if not self.nc.is_connected:
            logger.warning("Not connected to NATS, attempting to reconnect...")
            await self.connect()
        try:
            await self.nc.publish(subject, message.encode())
            logger.info(f"Published message to {subject}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise

    async def subscribe(self, subject, callback):
        if not self.nc.is_connected:
            logger.warning("Not connected to NATS, attempting to reconnect...")
            await self.connect()
        try:
            await self.nc.subscribe(subject, cb=callback)
            logger.info(f"Subscribed to {subject}")
        except Exception as e:
            logger.error(f"Failed to subscribe: {e}")
            raise

    async def close(self):
        try:
            await self.nc.close()
            logger.info("NATS connection closed")
        except Exception as e:
            logger.error(f"Failed to close NATS connection: {e}")
            raise


nats_provider = NatsProvider([config.settings.nats_url])
