from models.model_base import UserProfileBase, ContestBase
import datetime


class CodeforcesUserInfoModel(UserProfileBase):

    def __init__(self,
                 username=None,
                 max_rating=None,
                 current_rating=None,
                 solve_problems=None,
                 last_month_solutions=None,
                 last_contest_time=None,
                 latest_contests_ratings=None,
                 last_contests_name=None
                 ):
        self.username = username
        self.max_rating = max_rating
        self.current_rating = current_rating
        self.solve_problems = solve_problems
        self.last_month_solutions = last_month_solutions
        # 最近比赛（<10）的时间
        self.last_contest_time = last_contest_time
        # 元组形式分别为（rank，change，new_rating）
        self.latest_contests_ratings = latest_contests_ratings
        # 最近比赛（<10）的名称
        self.last_contests_name = last_contests_name

    def __repr__(self):
        return "----(CodeforcesUserInfoModel)---" \
               "\nusername: {}" \
               "\nmaxRating:{}" \
               "\ncurrentRating:{}".format(self.username, self.max_rating, self.current_rating)

    @property
    def latest_avg_contests_rating(self):
        """
            最近（<10）场比赛的平均rating
        """
        avg = 0
        if len(self.latest_contests_ratings) == 0:
            return None
        for item in self.latest_contests_ratings:
            avg += int(item[2])
        return avg / len(self.latest_contests_ratings)

    @property
    def latest_contest_time(self):
        """
            最近一场比赛的时间
            type : str
        """
        if len(self.last_contest_time) == 0:
            return None
        return self.last_contest_time[0]

    @property
    def late_contests_change(self):
        """
            最近（<10）场比赛的rating change
            type : tuple
        """
        if len(self.latest_contests_ratings) == 0:
            return None
        result = (item[1] for item in self.latest_contests_ratings)
        return result

    @property
    def late_contests_ratings(self):
        """
            最近（<10）场比赛的rating
            type : tuple
        """
        if len(self.latest_contests_ratings) == 0:
            return None
        result = (item[2] for item in self.latest_contests_ratings)
        return result

    @property
    def late_contests_rank(self):
        """
            最近比赛的一次rank排名
            type : tuple
        """
        if len(self.latest_contests_ratings) == 0:
            return None
        result = (item[0] for item in self.latest_contests_ratings)
        return result


class CodeforcesContestModel(ContestBase):

    def __init__(self, contest_name_list=None, contest_start_time_list=None, contest_length_list=None, \
                 contest_url_list=None):
        self.contest_name_list = contest_name_list
        self.contest_start_time_list = contest_start_time_list
        self.contest_length_list = contest_length_list
        self.contest_url_list = contest_url_list
        try:
            self.contests_info = [(x, y, z, u) for x, y, z, u in zip(contest_name_list, contest_start_time_list,
                                                                  contest_length_list, contest_url_list)]
        except TypeError:
            self.contests_info = []

    @property
    def today_contests(self):
        """
            获取今天的比赛信息
            :return -> tuple list [(name, time. length)]
        """
        _now = self.trans_to_date(datetime.datetime.now())
        contests = []
        try:
            for date_item in self.contests_info:
                trans_date_item = self.trans_to_date(date_item[1])
                if trans_date_item.day == _now.day and trans_date_item.month == _now.month \
                        and trans_date_item.year == _now.year:
                    contests.append(date_item)
        except TypeError:
            pass
        return contests

    @property
    def recent_contest(self):
        """
            获取最近的比赛信息（对标官网 recent contests）
        """
        pass
        return

    def __repr__(self):
        return self.contests_info.__repr__()
