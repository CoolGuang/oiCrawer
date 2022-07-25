
import datetime
import time


def change_to_str(func):
    def wrapper(cls, message):
        try:
            func(cls, message)
            return func
        except:
            if not isinstance(message, (int, str)):
                message = message.__repr__()
            func(cls, message)
            return func
    return wrapper


class Logger:

    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BlUE = '\033[94m'
    END = '\033[0m'

    @classmethod
    @change_to_str
    def waring(cls, message):
        print("{}WARING:{}{}".format(cls.YELLOW, message, cls.END))

    @classmethod
    @change_to_str
    def error(cls, message):
        print("{}ERROR:{}{}".format(cls.RED, message, cls.END))
        cls.save_to_local(message)

    @classmethod
    @change_to_str
    def common(cls, message):
        print("{}{}{}".format(cls.GREEN, message, cls.END))

    @classmethod
    @change_to_str
    def save_to_local(cls, message):
        with open("../error_log.txt", "a") as f:
            now_time = datetime.datetime.now()
            f.write("{}:\n".format(datetime.datetime.strftime(now_time,'%Y-%m-%d %H:%M:%S')))
            f.write("{}\n".format(message))

