import fastapi
import logging


def show(app: fastapi.FastAPI) -> None:
    routes_list = []
    for route in app.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            routes_list.append({"path": route.path, "methods": list(route.methods)})
            logging.info(f"API: '{route}'")
