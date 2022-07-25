
import os
import requests

from config.global_variable import *
from diy_logger import Logger

class CrawlerBase(object):
    """
        爬虫类， 参数接受url爬取对应信息
    """
    # 初始化
    def __init__(self):
        pass

    # 获取请求体， 父类获取方法
    @staticmethod
    def get_request_body(self, url=None, headers=None, username="defalut"):
        Logger.common("get url: {}".format(url))
        response = None
        result = None
        try:
            response = requests.get(url=url, headers=headers, allow_redirects=False, timeout=10)
            Logger.common("{}: request status :{}".format(username, response.status_code))
            if response.status_code == 200:
                result = response.content.decode("utf-8")
            elif response.status_code == 404:
                result = USER_NOT_EXIST
            # codeforces 用户不存在会重定向
            elif response.status_code == 302:
                result = USER_NOT_EXIST
            elif response.status_code == 408:
                result = URL_TIMEOUT
            else:
                result = COMMON_ERROR
        except requests.exceptions.ConnectionError:
            Logger.error("base_crawler line 36 : user->{} "
                         "ConnectionError".format(username))
        except requests.exceptions.URLRequired:
            Logger.error("base_crawler line 39 : user->{} "
                         "URLRequired".format(username))
        except requests.exceptions.Timeout:
            Logger.error("base_crawler line 42 : user->{} "
                         "request TimeoutError".format(username))
        except requests.exceptions.InvalidURL:
            Logger.error("base_crawler line 45 : user->{} "\
                         "request InvalidURL".format(username))
        except Exception:
            Logger.error("base_crawler line 48 : user->{} unknow error")
        finally:
            return result

    @staticmethod
    def check_result(result):
        if result == USER_NOT_EXIST:
            return False
        if result == URL_TIMEOUT:
            return False
        if result == COMMON_ERROR:
            return False
        return True
