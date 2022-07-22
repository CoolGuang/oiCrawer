
import datetime
import time


class Logger:

    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BlUE = '\033[94m'
    END = '\033[0m'

    @classmethod
    def waring(cls, message):
        print("{}WARING:{}{}".format(cls.YELLOW, message, cls.END))

    @classmethod
    def error(cls, message):
        print("{}ERROR:{}{}".format(cls.RED, message, cls.END))
        cls.save_to_local(message)

    @classmethod
    def common(cls, message):
        print("{}{}{}".format(cls.GREEN, message, cls.END))

    @classmethod
    def save_to_local(cls, message):
        with open("../error_log.txt", "a") as f:
            now_time = datetime.datetime.now()
            f.write("{}:\n".format(datetime.datetime.strftime(now_time,'%Y-%m-%d %H:%M:%S')))
            f.write("{}\n".format(message))

