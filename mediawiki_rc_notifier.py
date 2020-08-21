import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from json import loads
from threading import Thread
import socketserver

"""
Mediawiki RecentChange(RC) Notifier
A Nonebot Plugin

Version:
0.4.0-Beta
"""

# Configurable
IP='127.0.0.1' # ip: in string
PORT=10305 # port: in int
SITE_NAME='YOUR SITE NAME'
TARGET_ID=[11111111,222222222] # notice target user/group id
PRIVATE=False # user: True, group: False

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

class UdpHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        global cache
        data = self.rfile.read()
        data = loads(data.decode())
        if data["type"] not in ["edit", "new"]:
            return
        message = f'{data["id"]}: {"新建" if data["type"] == "new" else "修改"}页面 {data["title"]}'
        nonebot.log.logger.info('[MW RC No]'+message)
        cache.push(message)

class UdpThread(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.address = (ip, port)
        self.server = socketserver.ThreadingUDPServer(self.address, UdpHandler)
        nonebot.log.logger.info(f'[MW RC NO]Your UDP Server binds to {self.address}')

    def run(self):
        nonebot.log.logger.info("[MW RC No]Starting UDP Server Thread...")
        self.server.serve_forever()

async def notify(msg_list):
    if (len(msg_list)) == 0:
        return
    bot = nonebot.get_bot()
    message = f'{SITE_NAME}有条目更新!\n' + '\n'.join(msg_list)
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

@nonebot.on_startup
async def startup():
    nonebot.log.logger.info('[MW RC No]Thank you for using Mediawiki RC Notifier!')
    udp_server_thread = UdpThread(IP, PORT)
    udp_server_thread.start()

@nonebot.scheduler.scheduled_job('interval', seconds=30)
async def _():
    bot = nonebot.get_bot()
    await cache.fetch()
