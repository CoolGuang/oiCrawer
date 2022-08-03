from nonebot import on_command, CommandSession

"""
帮助文档
"""

DICT_COMMADN_LIST = {
    "[cft] " : "获取今天codeforces的比赛信息",
    "[cfc] " : "获取最近的codeforces比赛信息",
    "[cfs] " : "p [u] 查询codeforces的个人信息",
    "[help]" : "获取帮助文档"
}


@on_command('help', only_to_me=False, aliases=('helper', 'bot helper', 'bot help'))
async def search_profile(session: CommandSession):
    # 取得消息的内容，并且去掉首尾的空白符
    command = session.current_arg_text.strip()
    result = ""
    for item in DICT_COMMADN_LIST:
        result += "{} : {}\n".format(item, DICT_COMMADN_LIST[item])
    result += ":more for developing\n"
    await session.send(result)
