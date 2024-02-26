import uvicorn
import fastapi.applications
from fastapi import FastAPI
from config import settings
from domain.product.product_router import product_router

# Define the app at the module level
app: fastapi.applications.FastAPI = FastAPI(title=settings.app_name, version=settings.app_version)


@app.on_event("startup")
def startup_event():
    # Router definitions
    app.include_router(product_router)


if __name__ == "__main__":

    # the port is defined by command
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
