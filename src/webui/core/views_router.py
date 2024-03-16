from fastapi import APIRouter

from ui.view.home.router import home_router
from ui.view.monitor.router import router as monitor_router
from ui.view.product.router import router as product_router
from ui.view.simulator.router import router as simulator_router
from ui.view.type.router import router as type_router

main_router = APIRouter()

main_router.include_router(home_router)
main_router.include_router(simulator_router)
main_router.include_router(product_router)
main_router.include_router(monitor_router)
main_router.include_router(type_router)
