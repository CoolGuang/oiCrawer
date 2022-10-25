from .base_model import UserProfileBase, ContestBase

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
                 last_contests_name=None,
                 err_msg=None
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
        self.err_msg = err_msg

    def __repr__(self):
        if self.err_msg:
            return self.err_msg
        return "----(Codeforces个人信息)----" \
               "\n用户名: {}" \
               "\n最高Rating:{}" \
               "\n当前Rating:{}" \
               "\n最近一场rating波动:{}" \
               "\n最近一场比赛rank:{}" \
               "\n最近一场比赛时间:{}" \
               "\n最近一场比赛名称:{}" \
               "\n最近十场比赛平均rating:{}" \
               "\n总解决题目数量:{}" \
               "\n上个月解决题目数量:{}".format(self.username, self.max_rating, self.current_rating, self.latest_contest_change,
                                       self.latest_contests_rank, self.latest_contest_time, self.latest_contest_name,
                                       self.latest_avg_contests_rating, self.solve_problems, self.last_month_solutions)

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
    def latest_contest_name(self):
        """
            最近一场比赛的名称
            type : str
        """
        if len(self.last_contests_name) == 0:
            return None
        return self.last_contests_name[0]

    @property
    def latest_contest_change(self):
        """
            最近1 场比赛的rating change
            return type : str
        """
        if len(self.latest_contests_ratings) == 0:
            return None
        return self.latest_contests_ratings[0][1]

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
            最近比赛的(<10)rank排名
            type : tuple
        """
        if len(self.latest_contests_ratings) == 0:
            return None
        result = (item[0] for item in self.latest_contests_ratings)
        return result

    @property
    def latest_contests_rank(self):
        """
            最近1场比赛的rank排名
            return type: str
        """
        if len(self.latest_contests_ratings) == 0:
            return None
        return self.latest_contests_ratings[0][0]


class CodeforcesContestModel(ContestBase):

    def __init__(self, contest_name_list=None, contest_start_time_list=None, contest_length_list=None, \
                 contest_url_list=None, err_msg=None):
        self.contest_name_list = contest_name_list
        self.contest_start_time_list = contest_start_time_list
        self.contest_length_list = contest_length_list
        self.contest_url_list = contest_url_list
        # self.contest_info -> (名称，开始时间，持续时常，比赛链接）
        try:
            self.contests_info = [(x, y, z, u) for x, y, z, u in zip(contest_name_list, contest_start_time_list,
                                                                     contest_length_list, contest_url_list)]
        except TypeError:
            self.contests_info = []
        self.err_msg = err_msg

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

    def today_contests_string(self):
        if self.err_msg:
            return self.err_msg
        return self._get_contests_string(contest_list=self.today_contests)

    def recent_contest(self):
        if self.err_msg:
            return self.err_msg
        return self.contests_info

    def recent_contests_string(self):
        if self.err_msg:
            return self.err_msg
        return self._get_contests_string(contest_list=self.contests_info)

    def _get_contests_string(self, contest_list=None):
        result = ""
        if len(contest_list) == 0:
            result = "暂无任何比赛信息"
            return result
        for item in contest_list:
            result += "=========================\n"
            result += "比赛名称:{}\n" \
                      "开始时间:{}\n" \
                      "比赛时长:{}\n" \
                      "比赛链接:{}\n".format(item[0], item[1],
                                         item[2], item[3])
        return result
