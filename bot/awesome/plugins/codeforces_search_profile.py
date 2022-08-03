from nonebot import on_command, CommandSession

from tools import codeforces_crawler

"""
 提供codeforces比赛信息查询
"""


@on_command('cfs', only_to_me=False, aliases=('cf_search', 'cfp', 'cfsearch', 'cf查询'))
async def search_profile(session: CommandSession):
    # 取得消息的内容，并且去掉首尾的空白符
    command = session.current_arg_text.strip()
    if not command:
        username = (await session.aget(prompt='输入你要查询的codeforces的用户名')).strip()
        # 如果用户只发送空白符，则继续询问
        while not username:
            username = (await session.aget(prompt='用户名不可为空，请重新输入')).strip()
    await session.send("正在查询... 请稍后")
    crawler = codeforces_crawler.CodeforcesProfileCrawler(username=username)
    userinfo_model = await crawler.get_profile_info_model()
    await session.send(userinfo_model.__repr__())