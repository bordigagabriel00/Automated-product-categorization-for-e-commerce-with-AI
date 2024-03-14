from core.referemce import store


async def predict_dispatcher(msg):
    subject = msg.subject
    data = msg.data.decode()
    print(f"Sending msg '{subject}': {data}")
    await store.app.state.nc.publish("simulator.predict", message.encode())
    return {"message": "Message published to simulator.predict", "data": message}
