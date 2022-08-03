import datetime


class UserProfileBase(object):

    def __init__(self, username=None):
        self.username = username


class ContestBase(object):

    def __init__(self, contest_name=None, contest_begin_time=None):
        self.contest_begin_time = contest_begin_time

    def trans_to_date(self, date):
        """
            str date 转换成 datetime 格式
        """
        if isinstance(date, datetime.datetime):
            return date
        res_date = datetime.datetime.strptime(date, "%b/%d/%Y %H:%M")
        return res_date
