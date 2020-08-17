import socket
import os

"""
Mediawiki RecentChange(RC) UDP Server 
This is not nonebot plugin
Do not put it in plugins/
Put it in mybot/ (the parent directory of plugins/)
This file should run seperately in a screen

Version:
0.1.0-Alpha
"""

# Configurable UDP Address binding
PORT=10305
IP='0.0.0.0'
SITE_NAME='四叶草剧场百科'
PATH='plugins/mw_rc/'
if not os.path.exists(PATH):
    os.makedirs(PATH)

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (IP, PORT)
udp_socket.bind(address)

# Infinite Loop
while True:
    data, addr = udp_socket.recvfrom(1024)
    data = data.decode()
    with open(f'{PATH}rc_info.txt', 'a+') as f:
        f.seek(0)
        f.write(f'A new change occur on {SITE_NAME}: {data["id"]}: {data["title"]}\n')
