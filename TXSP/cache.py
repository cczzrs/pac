

class Data(object):

    db_pac = {}  # 爬取的数据 {参数规则, {url_base, [dbo],url_base, [dbo]}}

    txos = {}  # 一个参数规则对应一个操作对象


class sdatao(object):

    def __init__(self):
        self.db_dbo = []  # 对应数据库数据

        # 测试爬取分页列表，打印日志
        self.test_list_page_prints = []

        # 测试爬取详情页面，打印日志
        self.test_item_page_prints = []

        self.run_count = sets.TEST_RUN_COUNT  # 循环下一页数量

        self.test_list_page_threads = {}  # 所有爬虫线程集合 {thread-Name, thread}

        self.dbo_urls = {}  # 爬取列表页数据 {url, [dbo]}
        self.dbo_urls_b = True  # 数据有效性，结果是否可以入库

        self.dbo_resolve_key = {}  # 参数 key 入库所需的参数规则 key ，可根据 key 查看是否已有数据

        self.db_url_content = {}  # 爬取详情页数据 {url, db}

        self.downURLs = {}  # 下载资源（图片，文件等）到本地的 url 数据对象 {url, path}

        self.up_dbo_error_urls = {}  # 爬取异常的数据源，更新回数据库 {url, error}
