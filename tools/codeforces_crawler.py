import time

from base_crawler import CrawlerBase
import register_config

import models.codeforces_model as CFM
from config.global_variable import *

class CodeforcesCrawler(CrawlerBase):

    def __init__(self, username=None):
        self.username = username

    @register_config.ConfigBase.register(config_name="codeforces")
    def get_profile_info_body(self):
        config = register_config.ConfigBase.NAME_CONFIG_DICT["get_profile_info_body"]
        if not config:
            # TODO LOG()
            print("配置文件错误！")
            return None
        headers = config["headers"]
        url = ""
        for item in config["type_list"]:
            if item["type_name"] == "user_profile":
                url = item["urls"]

        url_profile = url[0] + "{}/".format(self.username)
        url_contest = url[1] + "{}/".format(self.username)
        profile_body_text = self.get_request_body(self, url=url_profile, headers=headers)
        time.sleep(1)
        contest_body_text = self.get_request_body(self, url=url_contest, headers=headers)

        # TODO need cancel, for test
        print (profile_body_text)
        print (contest_body_text)

        return profile_body_text, contest_body_text

    def deal_with_profile_body_contest(self, body=None):

        return None, None

    def deal_with_profile_body_info(self, body=None):

        return None, None, None

    def get_profile_info_model(self):
        profile_body_text, contest_body_text = self.get_profile_info_body()
        # TODO 根据类方法判断状态并返回
        max_rating, current_rating, solve_problems = \
            self.deal_with_profile_body_info(body=profile_body_text)
        last_contest_rank, latest_contests_ratings = \
            self.deal_with_profile_body_contest(contest_body_text)
        result_model = CFM.CodeforcesUserInfoModel(
            username=self.username,
            max_rating=max_rating,
            current_rating=current_rating,
            solve_problems=solve_problems,
            last_contest_rank=last_contest_rank,
            latest_contests_ratings=latest_contests_ratings,
        )

        return result_model

    @register_config.ConfigBase.register(config_name="codeforces")
    def get_contest_info(self):
        config = register_config.ConfigBase.NAME_CONFIG_DICT["get_profile_info"]
        pass


if __name__ == '__main__':
    # 测试
    crawler = CodeforcesCrawler("CCoolGuang")
    model = crawler.get_profile_info_model()

    print (model)