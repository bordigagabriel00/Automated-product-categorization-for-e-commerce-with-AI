import fastapi

from core.logger_provider import logger


def show(app: fastapi.FastAPI) -> None:
    routes_list = []
    for route in app.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            routes_list.append({"path": route.path, "methods": list(route.methods)})
            logger.info(f"API: '{route}'")
