import time


class Data(object):

    db_url_content = {}  # # 爬取详情页数据 {url, db}

    LPs = {}  # 一个 sessionid 对应一个操作对象 # {sessionid, lp}
    IPs = {}  # 一个 sessionid 对应一个操作对象 # {sessionid, ip}


class sdatao(object):

    def __init__(self):
        # 初始化时间
        self.time = time.time()

        # 测试爬取分页列表，打印日志数据对象
        self.test_list_page_prints = []

        # 测试爬取详情页面，打印日志数据对象
        self.test_item_page_prints = []

        # 下载资源（图片，文件等）到本地的 url 数据对象 {url, path}
        self.downURLs = {}

        # 爬取详情页数据 {url, [dbo]}
        self.dbo_urls = {}

        # 爬取详情页数据 {url, db}
        self.db_url_content = {}
