"""
async def Publish(topic, message):
    # Publish messages
    try:
        await main.appnc.publish(subject1, b'Msg from topic 1')
        await nc.publish(subject2, b'Msg from topic 2')
    except (ErrConnectionClosed, ErrTimeout) as e:
        print("Error publishing message:")
        return

"""
