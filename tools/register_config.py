import json


class ConfigBase(object):
    """
        获取配置的基类，该基类通过注解，把配置文件注入相应的爬取分类中。
    """
    NAME_CONFIG_DICT = {}
    # 工厂模式， 执行读取config之后的函数

    @classmethod
    def register(cls, config_name=None):
        def wrapper(func):
            if func.__name__ not in cls.NAME_CONFIG_DICT.keys():
                with open("./config/{}.json".format(config_name)) as f:
                    crawler_config = json.load(f)
                cls.NAME_CONFIG_DICT[config_name] = crawler_config
            return func
        return wrapper
