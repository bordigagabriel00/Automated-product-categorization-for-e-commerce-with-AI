import logging
from core.eventbus import nats_provider as nats, topic_health


async def monitor_message_handler(msg):
    subject = msg.subject
    data = msg.data.decode()
    logging.info(f"Received a message on '{subject}': {data}")
