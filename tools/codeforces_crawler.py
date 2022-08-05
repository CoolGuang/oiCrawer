import time

from tools import base_crawler

from tools import register_config

import models.codeforces_model as CFM
from config.global_variable import *

from bs4 import BeautifulSoup

from tools.diy_logger import Logger


class CodeforcesProfileCrawler(base_crawler.CrawlerBase):

    def __init__(self, username=None):
        self.username = username

    @register_config.ConfigBase.register(config_name="codeforces")
    def get_profile_info_body(self):
        config = register_config.ConfigBase.NAME_CONFIG_DICT["get_profile_info_body"]
        if not config:
            Logger.error("codeforces_crawler.py line 22 : codeforces config error!")
            return None
        headers = config["headers"]
        url = "123"
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
        Logger.waring(solve_problems)
        return max_rating, current_rating, last_month_solutions, solve_problems

    async def get_profile_info_model(self):
        profile_body_text, contest_body_text = self.get_profile_info_body()
        if not self.check_result(profile_body_text):
            return profile_body_text
        if not self.check_result(contest_body_text):
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


class CodeforcesContestCrawler(base_crawler.CrawlerBase):

    def __init__(self, username=None):
        self.username = username

    @register_config.ConfigBase.register(config_name="codeforces")
    def get_contest_info_body(self):
        config = register_config.ConfigBase.NAME_CONFIG_DICT["get_contest_info_body"]
        if not config:
            Logger.error("codeforces_crawler.py line 97 : codeforces config error!")
            return None
        headers = config["headers"]
        url = ""
        for item in config["type_list"]:
            if item["type_name"] == "latest_contest":
                url = item["urls"]
        contest_body_text = self.get_request_body(self, url=url[0], headers=headers)
        return contest_body_text

    def deal_with_contest_body(self, contest_body):
        contest_name_list = []
        contest_start_time_list = []
        contest_length_list = []
        contest_url_list = []
        soup = BeautifulSoup(markup=contest_body, features="lxml")
        contest_list = soup.select_one("div.datatable>div>table")
        contest_list = contest_list.select("tr")
        for contest in contest_list[1:]:

            contest_url_list.append("https://codeforces.com/contest/{}"\
                                    .format(contest['data-contestid'].strip('\n\r ')))
            items = contest.select("td")
            contest_name_list.append(items[0].string.strip('\n\r '))
            contest_start_time_list.append(items[2].select_one("span").string.strip('\n\r '))
            contest_length_list.append(items[3].string.strip('\n\r '))

        return contest_name_list, contest_start_time_list\
            , contest_length_list, contest_url_list

    async def get_contest_info_model(self):
        contest_body = self.get_contest_info_body()
        if not self.check_result(contest_body):
            return contest_body
        if contest_body is None:
            Logger.error("codeforces_crawler line 131 : variable is None")
            return COMMON_ERROR
        contest_name_list, contest_start_time_list, contest_length_list, contest_url_list = \
            self.deal_with_contest_body(contest_body=contest_body)
        res_model = CFM.CodeforcesContestModel(
            contest_name_list=contest_name_list,
            contest_start_time_list=contest_start_time_list,
            contest_length_list=contest_length_list,
            contest_url_list=contest_url_list
        )
        return res_model


if __name__ == '__main__':
    # 测试
    crawler = CodeforcesContestCrawler()
    model = crawler.get_contest_info_model()
    print(model.today_contests_string())
    print(model.recent_contests_string())
    # crawler_ = CodeforcesProfileCrawler(username="asda123")
    # print(crawler_.get_profile_info_model())