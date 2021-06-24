import asyncio
import time
from datetime import datetime

from models.config import CHANNELS


async def send_alive(bot, message):
    ws = bot._ws
    while(True):
        # datetime object containing current date and time
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        time.sleep(3400)
        await ws.send_privmsg(CHANNELS[0], message)
        #time.sleep(2400)


def between_callback(bot, message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(send_alive(bot, message))
    loop.close()
