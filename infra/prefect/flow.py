from prefect import flow, task
from prefect.deployments import Deployment

from datetime import timedelta


@task
def say_hello():
    print("Hello, World!")


@flow
def hello_world_flow():
    say_hello()


# Deployment
# Define an interval schedule to run the flow automatically, if needed.
# schedule = IntervalSchedule(interval=timedelta(hours=1))  # Example: run every hour.

if __name__ == "__main__":
    # Deploy the flow to Prefect Server
    deployment = Deployment.build_from_flow(
        flow=hello_world_flow,
        name="Hello World Flow Deployment",
        work_queue_name="TEST_WORK_QUEUEE",
        # schedule=schedule,  # Omit or modify this if you don't want a schedule
    )
    deployment.apply()

    # run the flow immediately
    hello_world_flow()
