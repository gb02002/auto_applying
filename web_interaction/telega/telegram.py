import os

from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel
import logging, asyncio
from .telega_post import check_posts, request_history
from env_stash import API_ID, API_HASH


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


async def main(channel_username):
    async with TelegramClient('session_name', API_ID, API_HASH[0]) as client:
        await client.start()
        await client.send_message('me', 'We are working babe!')
        channel = await client.get_entity(PeerChannel(channel_username))

        offset_id = 0

        while True:
            history = await request_history(client=client, channel=channel, offset_id=offset_id)

            if not history.messages:
                break

            await check_posts(history=history, client=client)

            offset_id = history.messages[-1].id

    await client.disconnect()


def telegram_entrypoint(channel):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(channel_username=channel))
