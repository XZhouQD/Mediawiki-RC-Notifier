from nonebot import on_command, CommandSession, permission
import os, requests

"""
Mediawiki RecentChange(RC) Notifier
A Nonebot Plugin
use with configurations

Version:
0.1.0-Alpha
"""

# Please configure this before using:
API_PATH='https://clover-wiki.com/wiki/api.php'

# manual lookup
@on_command('rc', aliases=('最近更改'), permission=permission.GROUP_ADMIN, only_to_me=False)
async def rc(session: CommandSession):
    rclimit = session.get('rclimit')
    result = await fetch_rc(rclimit)
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
    result_list = []
    for rc_item in j['query']['recentchanges']:
        result_list.append(f'{rc_item['rcid']}: {rc_item['title']}\n')
    result = ''.join(result_list)
    return result
