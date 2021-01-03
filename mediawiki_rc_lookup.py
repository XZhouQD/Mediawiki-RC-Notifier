from nonebot import on_command, CommandSession, permission, on_startup, log
import httpx

"""
Mediawiki RecentChange(RC) Lookup Plugin
A Nonebot Plugin
use with configurations

Version:
0.5.0
"""

# Please configure this before using:
API_PATH = 'https://your.domain/wiki/api.php'
SITE_NAME = 'YOUR SITE NAME'


async def fetch_rc(rclimit: int) -> str:
    url = f'{API_PATH}?action=query&list=recentchanges' \
          f'&rclimit={rclimit}&format=json'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if not resp.status_code == 200:
            return []
    r = httpx.get(url)
    j = r.json()
    result_list = []
    for rc_item in j['query']['recentchanges']:
        if rc_item["type"] not in ['edit', 'new']:
            continue
        result_list.append(
            f'操作{rc_item["rcid"]}: '
            f'{"新页面" if rc_item["type"] == "new" else "修改页面"} '
            f'{rc_item["title"]}\n')
    return result_list


@on_command('rc',
            aliases='最近更改',
            permission=permission.GROUP_ADMIN,
            only_to_me=False)
async def rc(session: CommandSession):
    rclimit = session.get('rclimit')
    result_list = await fetch_rc(rclimit)
    if not result_list:
        result = '未找到近期更新！'
    else:
        result = f'{SITE_NAME} 上的最近更改:\n' + ''.join(result_list)
    await session.send(result)


@rc.args_parser
async def rc_args_parser(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['rclimit'] = stripped_arg
        return


@on_startup
async def startup():
    log.logger.info('[MW RC Lo]Thank you for using Mediawiki RC Lookup!')
    log.logger.info(f'[MW RC Lo]Your API_PATH has been set to {API_PATH}')
    log.logger.info(f'[MW RC Lo]Your SITE_NAME has been set to {SITE_NAME}')
