
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
            response.raise_for_status()
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
            Logger.error("base_crawler line 38 : user->{} "
                         "ConnectionError".format(username))
        except requests.exceptions.URLRequired:
            Logger.error("base_crawler line 41 : user->{} "
                         "URLRequired".format(username))
        except requests.exceptions.Timeout:
            Logger.error("base_crawler line 44 : user->{} "
                         "request TimeoutError".format(username))
        except requests.exceptions.InvalidURL:
            Logger.error("base_crawler line 47 : user->{} "\
                         "request InvalidURL".format(username))
        except Exception:
            Logger.error("base_crawler line 50 : user->{} unknow error")
        finally:
            return result

    def check_result(*result):
        """
            返回传递参数是否存在于error状态
            return bool -> True:状态ok
        """
        for item in result:
            if item in STATE_ERROR_LIST:
                return False
        return True


