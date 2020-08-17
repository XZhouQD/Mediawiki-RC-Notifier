import nonebot
from aiocqhttp.exceptions import Error as CQHttpError

"""
Mediawiki RecentChange(RC) Notifier
A Nonebot Plugin
Make sure you run mediawiki_rc_udp_server first

Version:
Abandoned
0.1.0-Beta
"""

class NotificationCache:
    """The notification cache"""
    def __init__(self):
        self.cache = []
        self.path = 'plugins/mw_rc/rc_info.txt'
        # cleanup cache file
        with open(self.path, 'w') as f:
            pass
    
    def fetch(self):
        result_list = []
        with open(self.path, 'r') as f:
            for line in f.readlines():
                if line not in self.cache:
                    result_list.append(line)
                    self.cache.append(line)
        return ''.join(result_list)
        
notification_cache = NotificationCache()
TARGET_ID=[11111111,222222222] # notice target user/group id
PRIVATE=False #user: true, group: false

@nonebot.scheduler.scheduled_job('interval', seconds=10)
async def _():
    bot = nonebot.get_bot()
    message = notification_cache.fetch()
    if len(message) != 0:
        for target in TARGET_ID:
            if PRIVATE:
                try:
                    await bot.send_private_msg(user_id=target, message=message)
                except CQHttpError:
                    pass
            else:
                try:
                    await bot.send_group_msg(group_id=target, message=message)
                except CQHttpError:
                    pass
