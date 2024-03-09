import logging

topic_health = "health"


async def monitor_message_handler(msg):
    subject = msg.subject
    data = msg.data.decode()
    logging.info(f"Received a message on '{subject}': {data}")

