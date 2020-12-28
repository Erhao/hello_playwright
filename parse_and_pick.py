import argparse
from playwright import sync_playwright


class Parser():
    """ 解析命令 """

    def __init__(self):

        self.url = None
        self.parser = argparse.ArgumentParser(description="""
            A simple and flexible interface test script
            based on playwright and jsonpath_rw
            which can judge the existence of the field
            specify the value of the field and the count of the field and value
            output the statistical data of the interface response
            enter --help to view more
        """)
        # parser.add_argument('ta', metavar='a', type=int, nargs=2, help='test arg')
        self.parser.add_argument('--url', metavar='url', type=str, help='[str] the url you want to browse')
        self.parser.add_argument('--pick_key', metavar='pick_key', type=str, help='[str] the work you want to pick')
        self.args = self.parser.parse_args()

    def get_url(self):
        """ """

        return self.args.url

    def get_pick_key(self):
        """ """

        return self.args.pick_key


class Browser():
    """ play_wright请求 """

    def __init__(self, url):

        self.url = url
        self.browser_type = sync_playwright().start().chromium

    def start_browser(self):
        """ """

        self.browser = self.browser_type.launch()

    def get_resp(self):
        """ """

        page = self.browser.newPage()
        res = page.goto(self.url)
        return res.json()


    def stop_browser(self):
        """ """

        self.browser.close()


class Picker():
    """ Response解析 """

    def __init__(self):
        pass

    def pick_keyword(self, resp, keyword):
        """ 判断key是否存在, 如果存在则输出所有取值, 计数以及是否处于同一层级 """

        def recursive_pick(ins, res):
            if isinstance(ins, dict):
                for k, v in ins.items():
                    if k == keyword:
                        res.append(v)
                    elif isinstance(v, dict) or isinstance(v, list):
                        recursive_pick(v, res)
            elif isinstance(ins, list):
                for item in ins:
                    recursive_pick(item, res)
            return res
        res = recursive_pick(resp, [])
        return res


if __name__ == '__main__':

    parser = Parser()
    url = parser.get_url()
    pick_key = parser.get_pick_key()
    b = Browser(url)
    b.start_browser()
    resp = b.get_resp()
    picker = Picker()
    res = picker.pick_keyword(resp, pick_key)
    print('{}: {}'.format(pick_key, res))
    b.stop_browser()
