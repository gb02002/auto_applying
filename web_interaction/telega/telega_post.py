import os
import re
import asyncio

from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import Channel, InputPeerChannel, InputPeerUser
from telethon.tl.types.messages import ChannelMessages, Messages

from letter.entrypoint_letter import main as letter
from web_interaction.hh.hh_post import write_to_our_file

FILE_PATH = os.getenv("FILE_PATH")
MESSAGE_TEXT = os.getenv("MESSAGE_TEXT")
KEYWORD_PATTERN = r'(python|питон)'

SMTP_HOST = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SMTP_USER = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
FROM_EMAIL = os.getenv('SMTP_USERNAME')


user_id_regex = r'\B@+[a-zA-Z0-9\._]{4,20}\b'
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
link_pattern = r'\bhttps://\S+\b'
tg_link_pattern = r'\bhttps://t\.me/[a-zA-Z0-9_]{4,}\b'


async def request_history(client: TelegramClient, channel: InputPeerChannel, offset_id: int, limit=10, last_offset=0) \
        -> ChannelMessages:
    history = await client(GetHistoryRequest(
        peer=channel,
        offset_id=offset_id,
        offset_date=None,
        add_offset=0,
        limit=limit,
        max_id=0,
        min_id=0,
        hash=0
    ))
    return history


async def got_an_id(user_ids, client):
    tasks = [process_user_id(user_id, client) for user_id in user_ids]
    await asyncio.gather(*tasks)


async def process_user_id(user_id, client):
    try:
        user = await client.get_entity(user_id)
        if isinstance(user, InputPeerUser):
            await client.send_message(user, MESSAGE_TEXT)
            await client.send_file(user, FILE_PATH)
            print(f"Сообщение и документ отправлены пользователю с ID: {user_id}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения пользователю с ID: {user_id}. Ошибка: {e}")


async def got_a_tg_links(tg_links: list[str], client):
    tasks = [process_user_id(tg_link[13:], client) for tg_link in tg_links]
    await asyncio.gather(*tasks)


async def check_posts(history: ChannelMessages, client: TelegramClient) -> bool:
    for message in history.messages:
        try:
            if re.search(KEYWORD_PATTERN, message.message, re.IGNORECASE):
                tg_links = re.findall(tg_link_pattern, message.message)
                user_ids = re.findall(user_id_regex, message.message)
                emails = re.findall(email_regex, message.message)
                links = re.findall(link_pattern, message.message)

                if tg_links:
                    await got_a_tg_links(tg_links, client=client)

                if emails:
                    smtp = SMTP(hostname=SMTP_HOST, port=SMTP_PORT, use_tls=False)
                    await smtp.connect()
                    # await smtp.starttls()
                    await smtp.login(SMTP_USER, SMTP_PASSWORD)

                    tasks = [send_email(email, 'Job Post for Python', smtp=smtp) for email
                             in emails]

                    await asyncio.gather(*tasks)

                    await smtp.quit()

                if user_ids:
                    await got_an_id(user_ids, client=client)

                if not user_ids or emails and links:
                    for link in links:
                        write_to_our_file(link, message.message)
        except TypeError:
            pass

    return True


def create_message() -> str:
    # if input('If you want to use custom letter, press any char'):
    #     my_text = letter()
    # else:
    my_text = MESSAGE_TEXT
    return my_text


async def send_email(to_email, subject, smtp, content=MESSAGE_TEXT, file_path=FILE_PATH) -> bool:
    message = MIMEMultipart()
    message['From'] = FROM_EMAIL
    message['To'] = to_email
    message['Subject'] = subject

    message.attach(MIMEText(content, 'plain'))

    if file_path:
        with open(file_path, 'rb') as f:
            file_attachment = MIMEApplication(f.read(), Name=file_path)
        file_attachment['Content-Disposition'] = f'attachment; filename="{file_path}"'
        message.attach(file_attachment)

    await smtp.send_message(message)

    return True
