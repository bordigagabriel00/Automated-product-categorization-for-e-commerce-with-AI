from nats.aio.client import Client as NATS

import config

topic_predict_request = "predict.request"
topic_predict_response = "predict.response"
topic_health = "health"


class NatsProvider:
    def __init__(self, servers=None, max_reconnect_attempts=5, reconnect_time_wait=2):
        if servers is None:
            servers = ["nats://127.0.0.1:4222"]
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
            loggerwarning("Not connected to NATS, attempting to reconnect...")
            await self.connect()
        try:
            await self.nc.publish(subject, message.encode())
            logger.info(f"Published message to {subject}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise

    async def subscribe(self, subject, callback):
        if not self.nc.is_connected:
            loggerwarning("Not connected to NATS, attempting to reconnect...")
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
