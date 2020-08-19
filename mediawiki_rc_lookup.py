from nonebot import on_command, CommandSession, permission, get_bot, scheduler
import os, requests

"""
Mediawiki RecentChange(RC) Lookup Plugin
A Nonebot Plugin
use with configurations

Version:
0.2.1-Beta
"""

# Please configure this before using:
API_PATH='https://your-domain.com/wiki/api.php'
SITE_NAME='YOUR WIKI'
TARGET_ID=[11111111,222222222] # notice target user/group id
PRIVATE=False #user: True, group: False

async def fetch_rc(rclimit: int) -> str:
    url = f'{API_PATH}?action=query&list=recentchanges&rclimit={rclimit}&format=json'
    r = requests.get(url)
    j = r.json()
    result_list = []
    for rc_item in j['query']['recentchanges']:
        if rc_item["type"] not in ['edit', 'new']:
            continue
        result_list.append(f'操作{rc_item["rcid"]}: {"新页面" if rc_item["type"] == "new" else "修改页面"} {rc_item["title"]}\n')
    return result_list

class NotificationCache:
    """The notification cache"""
    def __init__(self):
        self.cache = []

    def get_cache(self):
        return self.cache

    async def fetch(self, rc=20):
        result_list = await fetch_rc(rc)
        try:
            diff = list(set(result_list).difference(set(self.cache)))
            diff.sort(reverse=True)
        except:
            diff = []
        self.cache = list(set(self.cache).union(set(result_list)))
        self.cache.sort()
        return ''.join(diff)

notification_cache = NotificationCache()

# Late Check - Ignore first round of shceduled checking!
first_run=True

@scheduler.scheduled_job('interval', seconds=30)
async def _():
    try:
        bot = get_bot()
        global first_run
        if first_run:
            msg = await notification_cache.fetch(rc=50)
            first_run = False
            return
        message = await notification_cache.fetch()
        if len(message) != 0:
            for target in TARGET_ID:
                if PRIVATE:
                    try:
                        await bot.send_private_msg(user_id=target, message=f'{SITE_NAME}有内容更新！\n'+message)
                    except CQHttpError:
                        pass
                else:
                    try:
                        await bot.send_group_msg(group_id=target, message=f'{SITE_NAME}有内容更新！\n'+message)
                    except CQHttpError:
                        pass
    except:
        pass

# manual lookup
@on_command('rc', aliases=('最近更改'), permission=permission.GROUP_ADMIN, only_to_me=False)
async def rc(session: CommandSession):
    rclimit = session.get('rclimit')
    result_list = await fetch_rc(rclimit)
    result = f'{SITE_NAME} 上的最近更改:\n' + ''.join(result_list)
    await session.send(result)

@rc.args_parser
async def rc_args_parser(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['rclimit'] = stripped_arg
        return
