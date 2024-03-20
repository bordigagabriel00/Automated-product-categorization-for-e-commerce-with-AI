import json
import pathlib
from typing import Any

import fastapi.applications
import nats
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.logger import logger as fastapi_logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.simulator.model import RequestModel
from config import settings
from core import api_provider
from core import setup
from core.arangodb_provider import ArangoDBConnection
from core.environment import ConfigProvider
from core.logger_provider import logger

origins = [
    "*",
]

# Define the app at the module level
app: fastapi.applications.FastAPI = FastAPI(title=settings.app_name,
                                            description=settings.description,
                                            version=settings.app_version)
fastapi_logger.handlers = logger.handlers
fastapi_logger.setLevel(logger.level)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite todos los orígenes
    allow_credentials=True,  # Permite cookies
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los encabezados
)

# Define db connection
db_connection = Any

# Define static section
BASE_STATIC_DIR = pathlib.Path(__file__).parent / 'ui' / 'static'
app.mount("/static", StaticFiles(directory=BASE_STATIC_DIR), name="static")

environment = ConfigProvider()


async def init_options(option: ConfigProvider) -> None:
    option.set_config("app", "title", settings.app_name)
    option.set_config("app", "description", settings.description)
    option.set_config("app", "version", settings.app_version)
    option.set_config("app", "base_static_dir", BASE_STATIC_DIR)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    async def response_predict_handler(msg):
        logger.info(f"Response model: '{msg.data.decode()}'")
        await websocket.send_text(msg.data.decode())

    nc = await nats.connect(settings.nats_url)
    await nc.subscribe("response.predict", cb=response_predict_handler)

    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        request = json.loads(data)

        request_instance = RequestModel(payload=request)
        json_request = request_instance.model_dump_json()

        logger.info(f"json request model: '{json_request}'")

        subject = "request.predict"
        message = json_request

        await nc.publish(subject, message.encode())


@app.on_event("startup")
async def startup_event():
    global db_connection

    # Define environment
    await init_options(environment)
    # Define View, Routers
    await setup.init(app)
    # Show api definitions
    api_provider.show(app)

    # Verify connection
    try:
        db_connection = ArangoDBConnection.get_instance(settings.arango_url,
                                                        settings.username,
                                                        settings.password,
                                                        settings.product_model_db)

        if db_connection.verify_connection():
            logger.info("DB: The ArangoDB connection is active and verified.")
        else:
            logger.error("DB: The ArangoDB connection could not be verified.")
    except Exception as e:
        logger.error(f"Failed to initialize ArangoDB connection: {e}")

    collections = db_connection.db.collections()
    logger.info("Successfully connected to ArangoDB!")
    logger.info(collections)


if __name__ == "__main__":
    # the port is defined by command
    uvicorn.run("main:app", host="0.0.0.0", reload=True)

"""
TODO: Predict
TODO: DockerFile
TODO: test
TODO: 
"""
