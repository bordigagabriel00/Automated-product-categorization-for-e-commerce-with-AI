import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers


async def run():
    # Connect to NATS
    nc = NATS()

    try:
        # Attempt to connect to the NATS server
        await nc.connect("nats://localhost:4222")
    except ErrNoServers as e:
        print("Could not connect to NATS: ")
        return

        # Define subjects
    subject1 = "test.topic1"
    subject2 = "test.topic2"

    # Subscribe to topics
    async def message_handler1(msg):
        print(f"Received a message on '{msg.subject}': {msg.data.decode()}")

    async def message_handler2(msg):
        print(f"Received a message on '{msg.subject}': {msg.data.decode()}")

    await nc.subscribe(subject1, cb=message_handler1)
    await nc.subscribe(subject2, cb=message_handler2)

    # Publish messages
    try:
        await nc.publish(subject1, b'Msg from topic 1')
        await nc.publish(subject2, b'Msg from topic 2')
    except (ErrConnectionClosed, ErrTimeout) as e:
        print("Error publishing message:")
        return

        # Wait for messages to be processed
    await asyncio.sleep(1)

    # Close the connection
    try:
        await nc.close()
    except ErrConnectionClosed as e:
        print("Error closing NATS connection: ")
        return


if __name__ == '__main__':
    asyncio.run(run())
