
import os
import requests


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
        try:
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                return response.content.decode("utf-8")
            else:
                return None
        except Exception as e:
            # TODO 文本获取失败
            print ("(param:{}), request error!".format(username))
        finally:
            return None
