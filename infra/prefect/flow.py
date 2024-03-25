from prefect import flow, task, get_run_logger
import asyncio



@task
async def activate_task():
    print("Hello, Prefect!")


@flow
async def activate_flow():
    logger = get_run_logger()
    await activate_task()

if __name__ == "__main__":
    asyncio.run(activate_flow())
