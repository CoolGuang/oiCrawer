from .base_crawler import CrawlerBase
from tools import register_config, Logger
from models import CodeforcesContestModel, CodeforcesUserInfoModel
from config import COMMON_ERROR

from bs4 import BeautifulSoup


class CodeforcesProfileCrawler(CrawlerBase):

    def __init__(self, username=None):
        self.username = username
        self._result_model = None # final result
        self.timer = None # may be extend timer[now not apply]
        self.profile_url = None
        self.contest_url = None
        self.headers = None
        self._preLoad()

    @register_config.ConfigBase.register(config_name="codeforces_profile")
    def _preLoad(self):
        config = register_config.ConfigBase.NAME_CONFIG_DICT["codeforces_profile"]
        if not config:
            Logger.error("codeforces config error!")
            return None
        self.profile_url = config["profile_url"]
        self.contest_url = config["contest_url"]
        self.headers = config["headers"]

    @staticmethod
    def _deal_with_contest_body(body=None):
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

    @staticmethod
    def _deal_with_profile_body(body=None):
        soup = BeautifulSoup(markup=body, features="lxml")
        current_rating = soup.select_one("div.info>ul>li>span").string
        max_rating = soup.select("div.info>ul>li>span.smaller>span")[1].string
        problems_set = soup.select("div._UserActivityFrame_footer>div>div."
                                   "_UserActivityFrame_counter>div._UserActivityFrame_counterValue")
        last_month_solutions = problems_set[2].string
        solve_problems = problems_set[0].string
        Logger.waring(solve_problems)
        return max_rating, current_rating, last_month_solutions, solve_problems

    def _get_model(self) -> CodeforcesUserInfoModel:
        # error judge
        profile_body = self.get_request_body(url=self.profile_url,
                                             headers=self.headers, username=self.username)
        if not self.check_result(profile_body):
            return CodeforcesUserInfoModel(err_msg=profile_body)
        contest_body = self.get_request_body(url=self.contest_url,
                                             headers=self.headers, username=self.username)
        if not self.check_result(contest_body):
            return CodeforcesUserInfoModel(err_msg=contest_body)

        if profile_body is None or contest_body is None:
            Logger.error("variable is None")
            return COMMON_ERROR
        # error judge
        max_rating, current_rating, last_month_solutions, solve_problems = \
            self._deal_with_profile_body(body=profile_body)
        last_contests_name, latest_contests_ratings, last_contest_time = \
            self._deal_with_contest_body(body=contest_body)
        result_model = CodeforcesUserInfoModel(
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

    @property
    def result_info(self) -> str:
        if self._result_model is None:
            self._result_model = self._get_model()
        result_info = self._result_model.__repr__()
        return result_info

    @property
    def result_model(self):
        if self._result_model is None:
            self._result_model = self._get_model()
        return self._result_model


class CodeforcesContestCrawler(CrawlerBase):

    def __init__(self, username=None):
        self.username = username
        self.headers = None
        self.profile_url = None
        self._preLoad()
        self._result_model = None

    @register_config.ConfigBase.register(config_name="codeforces_contest")
    def _preLoad(self):
        config = register_config.ConfigBase.NAME_CONFIG_DICT["codeforces_contest"]
        if not config:
            Logger.error("codeforces_crawler.py line 97 : codeforces config error!")
            return None
        self.headers = config["headers"]
        self.profile_url = config["profile_url"]

    @staticmethod
    def deal_with_contest_body(contest_body):
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

    def _get_model(self) -> CodeforcesContestModel:
        contest_body = self.get_request_body(url=self.profile_url, headers=self.headers)
        if not self.check_result(contest_body):
            return CodeforcesContestModel(err_msg=contest_body)
        if contest_body is None:
            return CodeforcesContestModel(err_msg=COMMON_ERROR)
        contest_name_list, contest_start_time_list, contest_length_list, contest_url_list = \
            self.deal_with_contest_body(contest_body=contest_body)
        res_model = CodeforcesContestModel(
            contest_name_list=contest_name_list,
            contest_start_time_list=contest_start_time_list,
            contest_length_list=contest_length_list,
            contest_url_list=contest_url_list
        )
        return res_model

    @property
    def result_model(self):
        if self._result_model is None:
            self._result_model = self._get_model()
        return self._result_model


if __name__ == '__main__':
    # 测试
    crawler = CodeforcesContestCrawler()
    model = crawler.result_model
    print(model.today_contests_string())
    crawler_ = CodeforcesProfileCrawler(username="CCoolGuang")
    model = crawler_.result_info
    print(model)