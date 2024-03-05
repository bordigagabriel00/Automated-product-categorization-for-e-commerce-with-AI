import uvicorn
import fastapi.applications
from fastapi import FastAPI
from config import config
from api.health.router import health_router
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
import asyncio

# Define the app at the module level
app: fastapi.applications.FastAPI = FastAPI(title=config.app_name,
                                            description=config.description,
                                            version=config.app_version)


@app.on_event("startup")
async def startup_event():
    # Subscribe Service
    app.state.nc = NATS()
    try:
        # Attempt to connect to the NATS server
        await app.state.nc.connect(config.nats_url)
    except ErrNoServers as e:
        print("Could not connect to NATS: ")
        return

    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        print(f"Received a message on '{subject}': {data}")

    await app.state.nc.subscribe("simulator.predict", cb=message_handler)

    # Health definitions
    app.include_router(health_router)


if __name__ == "__main__":
    # the port is defined by command
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
