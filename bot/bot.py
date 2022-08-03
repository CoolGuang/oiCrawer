import nonebot
from os import path
import config_

if __name__ == '__main__':
    nonebot.init(config_)
    #nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'awesome', 'plugins'),
        'awesome.plugins'
    )
    nonebot.run()