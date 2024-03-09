import logging

from core.eventbus import nats_provider as nats, topic_predict_request


async def predict_response_handler(msg):
    subject = msg.subject
    data = msg.data.decode()

    await nats.publish(topic_predict_request, " Send Message from api predict")
    await nats.publish(topic_predict_request, " Send Message from api predict")
    logging.info(f"Received a message on '{subject}': {data}")
