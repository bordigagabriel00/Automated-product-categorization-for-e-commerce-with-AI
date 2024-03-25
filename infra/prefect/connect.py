from prefect import flow, get_run_logger
from prefect.blocks.system import JSON
import asyncio


# export PREFECT_API_URL=http://127.0.0.1:4200/api
@flow(name="Obtener Bloque Prefect")
async def obtener_bloque_prefect(block_name: str):
    logger = get_run_logger()

    block = await JSON.load(block_name)

    # Log del contenido del bloque (cambia esto según lo que desees hacer con el bloque)
    logger.info(f"Contenido del bloque '{block_name}' recibido")


if __name__ == "__main__":
    asyncio.run(obtener_bloque_prefect("webui-config"))
