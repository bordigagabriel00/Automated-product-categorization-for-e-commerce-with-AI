import logging
import json
from api.simulator.model import PredictRequest
from core.eventbus import nats_provider as nats, topic_predict_response

from nats.aio.client import Client as NATS
from nats.js.api import JetStream, StorageType, KeyValueConfig, KeyValueStatus



async def predict_request_handler(msg):
    data = json.loads(msg.data.decode())
    logging.info(f"Received subject request: {msg.subject} ")
    logging.info(f"Received reply request: {msg.reply} ")
    logging.info(f"Received predict request: {data}")

    js = JetStream(nats.nc)

        # Create a KV
    kv = await js.create_key_value(bucket='MY_KV')
    
        # Set and retrieve a value
    await kv.put('hello', b'world')
    entry = await kv.get('hello')
    print(f'KeyValue.Entry: key={entry.key}, value={entry.value}')
        # KeyValue.Entry: key=hello, value=world
    






    predict_response = {"predict_id": "2323", "data": ""}
    # data = predict.data.decode()
    # logging.info(f"Received predict data: {data}")

    data_prediction = {"category": "test",
                       "probability": "99.9"}
    predict_response["data"] = json.dumps(data_prediction)
    logging.info(f"Predict process")
    try:
        # await nats.publish(topic_predict_response, json.dumps(predict_response))
        logging.info(f"Predict result: {predict_response} ")
    except Exception as e:
        logging.error(f"Predict request error: {e}")
