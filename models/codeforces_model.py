
from models.model_base import UserProfileBase, ContestBase


class CodeforcesUserInfoModel(UserProfileBase):

    def __init__(self,
                 username=None,
                 max_rating=None,
                 current_rating=None,
                 solve_problems=None,
                 last_contest_rank=None,
                 latest_contests_ratings=None,
                 ):
        self.username = username
        self.max_rating = max_rating
        self.current_rating = current_rating
        self.solve_problems = solve_problems
        self.last_contest_rank = last_contest_rank
        self.latest_contests_ratings = latest_contests_ratings

    def __repr__(self):
        return "----(CodeforcesUserInfoModel)---" \
               "\nusername: {}" \
               "\nmaxRating:{}" \
               "\ncurrentRating:{}".format(self.username, self.max_rating, self.current_rating)

    @property
    def latest_avg_contests_rating(self):
        avg = 0
        for item in self.latest_contests_ratings:
            avg += item
        return avg / len(self.latest_contests_ratings)
