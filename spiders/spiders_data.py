# 数据结构模板，多个 cache 类模仿


class sdata(object):

    # 测试爬取分页列表，打印日志数据对象
    test_list_page_prints = []

    # 测试爬取详情页面，打印日志数据对象
    test_item_page_prints = []

    # 下载资源（图片，文件等）到本地的 url 数据对象 {url, path}
    downURLs = {}

    # 爬取详情页数据 {url, [dbo]}
    dbo_urls = {}

    # 爬取详情页数据 {url, db}
    db_url_content = {}

