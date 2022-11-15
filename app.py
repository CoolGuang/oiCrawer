from crawler import CodeforcesContestCrawler, CodeforcesProfileCrawler

if __name__ == '__main__':

    crawler_ = CodeforcesProfileCrawler(username="CCoolGuang")
    model = crawler_.result_model
    print(model)

