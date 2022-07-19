from base_crawler import CrawlerBase
import register_config

class CodeforcesCrawler(CrawlerBase):

    def __init__(self, username=None):
        self.username = username

    @register_config.ConfigBase.register(config_name="codeforces")
    def get_profile_info(self):
        config = register_config.ConfigBase.NAME_CONFIG_DICT["get_profile_info"]
        if not config:
            # TODO LOG()
            print("配置文件错误！")
            return None
        headers = config["headers"]
        url = ""
        for item in config["type_list"]:
            if item["type_name"] == "user_profile":
                url = item["url"]
        url = url + "{}/".format(self.username)
        body_text = self.get_request_body(self, url=url, headers=headers)

    def deal_with_profile_body(self, body=None):
        pass

    @register_config.ConfigBase.register(config_name="codeforces")
    def get_contest_info(self):
        config = register_config.ConfigBase.NAME_CONFIG_DICT["get_profile_info"]
        pass


if __name__ == '__main__':
    # 测试
    crawler = CodeforcesCrawler("CCoolGuang")
    crawler.get_profile_info()
