import socket
import os
from json import loads

"""
Mediawiki RecentChange(RC) UDP Server 
This is not nonebot plugin
Do not put it in plugins/
Put it in the parent directory of plugins/, at the level of bot.py
This file should run seperately in a screen

Version:
Abandoned
0.1.0-Beta
"""

# Configurable UDP Address binding
PORT=10305
IP='0.0.0.0'
SITE_NAME='YOUR WIKI NAME'
PATH='plugins/mw_rc/'
if not os.path.exists(PATH):
    os.makedirs(PATH)

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (IP, PORT)
udp_socket.bind(address)

with open(f'{PATH}rc_info.txt', 'w') as f:
    pass

# Infinite Loop
while True:
    data, addr = udp_socket.recvfrom(1024)
    data = data.decode()
    print(f'{addr}: {data})
    f = open(f'{PATH}rc_info.txt', 'a+')
    f.seek(0)
    data = loads(data)
    f.write(f'{SITE_NAME}有条目更新! {data["id"]}: {data["title"]}\n')
    f.close()
