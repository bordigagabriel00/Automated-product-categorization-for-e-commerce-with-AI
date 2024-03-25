from core.logger_provider import logger


async def monitor_message_handler(msg):
    subject = msg.subject
    data = msg.data.decode()
    logger.info(f"Received a message on '{subject}': {data}")
