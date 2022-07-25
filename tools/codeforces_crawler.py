import time

from base_crawler import CrawlerBase
import register_config

import models.codeforces_model as CFM
from config.global_variable import *

from bs4 import BeautifulSoup

from diy_logger import Logger

class CodeforcesCrawler(CrawlerBase):

    def __init__(self, username=None):
        self.username = username

    @register_config.ConfigBase.register(config_name="codeforces")
    def get_profile_info_body(self):
        config = register_config.ConfigBase.NAME_CONFIG_DICT["get_profile_info_body"]
        if not config:
            Logger.error("codeforces_crawler.py line 22 : codeforces config error!")
            return None
        headers = config["headers"]
        url = ""
        for item in config["type_list"]:
            if item["type_name"] == "user_profile":
                url = item["urls"]

        url_profile = url[0] + "{}/".format(self.username)
        url_contest = url[1] + "{}/".format(self.username)
        profile_body_text = self.get_request_body(self, url=url_profile, headers=headers, username=self.username)
        time.sleep(1)
        contest_body_text = self.get_request_body(self, url=url_contest, headers=headers, username=self.username)

        return profile_body_text, contest_body_text

    def deal_with_profile_body_contest(self, body=None):
        soup = BeautifulSoup(markup=body, features="lxml")
        result_set = soup.select("div.datatable>div>table>tbody>tr")
        last_contests_name = []
        latest_contests_ratings = []
        last_contest_time = []
        if len(result_set) > 10:
            result_set = result_set[:10]
        for item in result_set:
            contests = item.select("td")
            rating_t = (contests[3].string, contests[5].select_one("span").string, contests[6].string.strip('\r\n '))
            latest_contests_ratings.append(rating_t)
            last_contest_time.append(contests[2].text.strip('\r\n '))
            last_contests_name.append(contests[1].select_one("a").string.strip('\r\n '))
        return last_contests_name, latest_contests_ratings, last_contest_time

    def deal_with_profile_body_info(self, body=None):
        soup = BeautifulSoup(markup=body, features="lxml")
        current_rating = soup.select_one("div.info>ul>li>span").string
        max_rating = soup.select("div.info>ul>li>span.smaller>span")[1].string
        problems_set = soup.select("div._UserActivityFrame_footer>div>div."
                                           "_UserActivityFrame_counter>div._UserActivityFrame_counterValue")
        last_month_solutions = problems_set[2].string
        solve_problems = problems_set[0].string

        return max_rating, current_rating, last_month_solutions, solve_problems

    def get_profile_info_model(self):
        profile_body_text, contest_body_text = self.get_profile_info_body()
        if profile_body_text in STATE_ERROR_LIST:
            return profile_body_text
        if contest_body_text in STATE_ERROR_LIST:
            return contest_body_text
        if profile_body_text is None or contest_body_text is None:
            Logger.error("codeforces_crawler line 54 : variable is None")
            return COMMON_ERROR
        max_rating, current_rating, last_month_solutions, solve_problems = \
            self.deal_with_profile_body_info(body=profile_body_text)
        last_contests_name, latest_contests_ratings, last_contest_time = \
            self.deal_with_profile_body_contest(body=contest_body_text)
        result_model = CFM.CodeforcesUserInfoModel(
            username=self.username,
            max_rating=max_rating,
            current_rating=current_rating,
            solve_problems=solve_problems,
            last_month_solutions=last_month_solutions,
            last_contest_time=last_contest_time,
            latest_contests_ratings=latest_contests_ratings,
            last_contests_name=last_contests_name,
        )
        return result_model

    @register_config.ConfigBase.register(config_name="codeforces")
    def get_contest_info_body(self):
        config = register_config.ConfigBase.NAME_CONFIG_DICT["get_profile_info"]
        pass


if __name__ == '__main__':
    # 测试
    crawler = CodeforcesCrawler("CCoolGuang")
    model = crawler.get_profile_info_model()
    Logger.waring(model.username)
    Logger.waring(model.max_rating)
    Logger.waring(model.last_contests_name)

    for item in model.late_contests_change:
        Logger.waring(item)

    Logger.waring(model.latest_contests_ratings)
    Logger.waring(model.latest_avg_contests_rating)
    Logger.waring(model.latest_contest_time)