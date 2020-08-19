import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from json import loads
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread

"""
Mediawiki RecentChange(RC) Notifier
A Nonebot Plugin

Version:
0.3.0-Beta
"""

# Configurable
IP='127.0.0.1' # ip: in string
PORT=10305 # port: in int
SITE_NAME='YOUR SITE NAME'
TARGET_ID=[11111111,222222222] # notice target user/group id
PRIVATE=False # user: True, group: False

class udpThread(Thread):
    def __init__(self, ip, port, cache):
        Thread.__init__(self)
        self.address = (ip, port)
        self.server = socket(AF_INET, SOCK_DGRAM)
        self.server.bind(self.address)
        nonebot.log.logger.info(f'[MW RC NO]Your UDP Server binds to {self.address}')
        self.cache = cache

    def run(self):
        nonebot.log.logger.info("[MW RC No]Starting UDP Server Thread...")
        while True:
            try:
                data, addr = self.server.recvfrom(2048)
                data = loads(data.decode())
                if data["type"] not in ["edit", "new"]:
                    continue
                message = f'{SITE_NAME}有条目更新! {data["id"]}: {"新建" if data["type"] == "new" else "修改"}页面 {data["title"]}'
                nonebot.log.logger.info('[MW RC No]'+message)
                self.cache.push(message)
            except:
                continue

async def notify(msg_list):
    if (len(msg_list)) == 0:
        return
    bot = nonebot.get_bot()
    message = '\n'.join(msg_list)
    for target in TARGET_ID:
        if PRIVATE:
            try:
                await bot.send_private_msg(user_id=target, message=message)
                nonebot.log.logger.info("[MW RC No]Message sent out!")
            except CQHttpError:
                pass
        else:
            try:
                await bot.send_group_msg(group_id=target, message=message)
                nonebot.log.logger.info("[MW RC No]Message sent out!")
            except CQHttpError:
                pass

class Cache():
    def __init__(self):
        self.queue = []

    async def fetch(self):
        n_list = self.queue.copy()
        self.queue = []
        await notify(n_list)

    def push(self, item):
        self.queue.append(item)

cache = Cache()

@nonebot.on_startup
async def startup():
    nonebot.log.logger.info('[MW RC No]Thank you for using Mediawiki RC Notifier!')
    udp_server_thread = udpThread(IP, PORT, cache)
    udp_server_thread.start()

@nonebot.scheduler.scheduled_job('interval', seconds=30)
async def _():
    bot = nonebot.get_bot()
    await cache.fetch()
