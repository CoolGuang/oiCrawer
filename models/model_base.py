

class UserProfileBase(object):

    def __init__(self, username=None):
        self.username = username


class ContestBase(object):

    def __init__(self, contest_name=None, contest_begin_time=None):
        self.contest_begin_time = contest_begin_time
