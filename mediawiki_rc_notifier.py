from nonebot import get_bot
from aiocqhttp.exceptions import Error as CQHttpError
import socket

"""
Mediawiki RecentChange(RC) Notifier
A Nonebot Plugin
use with configurations

Version:
0.1.0-Alpha
"""

async def notice(decoded_data, target_id, is_private=True):
    bot = get_bot()
    message = f'A new change occur on {SITE_NAME}: {decoded_data["id"]}: {decoded_data["title"]}'
    if is_private:
        try:
            await bot.send_private_msg(user_id=target_id, message=message)
        except CQHttpError:
            pass
    else:
        try:
            await bot.send_group_msg(group_id=target_id, message=message)
        except CQHttpError:
            pass

# Configurable UDP Address binding
PORT=10305
IP='127.0.0.1'
SITE_NAME='四叶草剧场百科'
TARGET_ID=394626288 # notice target user/group id
PRIVATE=True #user: true, group: false

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (IP, PORT)
udp_socket.bind(address)

# Infinite Loop
while True:
    data, addr = udp_socket.recvfrom(1024)
    data = data.decode()
    notice(data, TARGET_ID, PRIVATE)
