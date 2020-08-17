from nonebot import on_command, CommandSession, permission
import os, requests

"""
Mediawiki RecentChange(RC) Lookup Plugin
A Nonebot Plugin
use with configurations

Version:
0.2.0-Alpha
"""

# Please configure this before using:
API_PATH='https://your-domain.com/wiki/api.php'
SITE_NAME='Your sitename'

class NotificationCache:
    """The notification cache"""
    def __init__(self):
        self.cache = []
    
    async def fetch(self):
        result_list = await fetch_rc(20)
        diff = list(set(result_list).difference(set(self.cache)))
        self.cache = list(set(self.cache).union(set(result_list)))
        return ''.join(diff)
        
notification_cache = NotificationCache()
notification_cache.fetch()
# Please configure this before using:
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

# manual lookup
@on_command('rc', aliases=('最近更改'), permission=permission.GROUP_ADMIN, only_to_me=False)
async def rc(session: CommandSession):
    rclimit = session.get('rclimit')
    result_list = await fetch_rc(rclimit)
    result = ''.join(result_list)
    await session.send(result)

@rc.args_parser
async def rc_args_parser(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    
    if session.is_first_run:
        if stripped_arg:
            session.state['rclimit'] = stripped_arg
        return
        
async def fetch_rc(rclimit: int) -> str:
    url = f'{API_PATH}?action=query&list=recentchanges&rclimit={rclimit}&format=json'
    r = requests.get(url)
    j = r.json()
    result_list = [f'Recent Changes on {SITE_NAME}:\n']
    for rc_item in j['query']['recentchanges']:
        if rc_item["type"] not in ['edit', 'new']:
            continue
        result_list.append(f'操作{rc_item["rcid"]}: {"新页面" if rc_item["type"] == "new" else "修改页面"} {rc_item["title"]}\n')
    return result_list
