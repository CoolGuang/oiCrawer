from nonebot import on_command, CommandSession

from crawler import codeforces_crawler

"""
 提供codeforces比赛信息查询
"""


# 最近的比赛信息
@on_command('cf', only_to_me=False, aliases=('cfl', 'cfc', 'cf contests', 'cf_contests', 'cf list', 'cf_list'))
async def search_profile(session: CommandSession):
    # 取得消息的内容，并且去掉首尾的空白符
    command = session.current_arg_text.strip()
    crawler = codeforces_crawler.CodeforcesContestCrawler()
    contest_model = await crawler.get_contest_info_model()
    await session.send(contest_model.recent_contests_string())


# 当前的比赛信息
@on_command('cft', only_to_me=False, aliases=('cft', 'cf today'))
async def search_profile(session: CommandSession):
    # 取得消息的内容，并且去掉首尾的空白符
    command = session.current_arg_text.strip()
    crawler = codeforces_crawler.CodeforcesContestCrawler()
    contest_model = await crawler.get_contest_info_model()
    await session.send(contest_model.today_contests_string())
