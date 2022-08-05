from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event

test = on_command('hello', priority=2)


# 测试发送指定消息 机器人回复的内容 注意发送指令时要加/  /hello

@test.handle()
async def hello(bot: Bot, event: Event, state: dict):
    print(event)
    await bot.send(
        event=event,
        message='hello',
    )
