import threading, pickle, json
from pac import urls
from core import SpiderBase
from core.models import SpidersBaseSource
from django.shortcuts import render, HttpResponse


def index(request):
    # request.GET
    # request.POST
    request.session['LP'] = str(pickle.dumps(LP()))
    request.session['IP'] = str(pickle.dumps(IP()))
    return render(request, 'core/index.html')


class TXT(object):
    tt = 'hello!'

    def p(self):
        return 'P'


def test(request):
    # request.GET
    # request.POST
    request.session.TX = TXT()

    return HttpResponse(str(request.session.TX.tt))


def test2(request):
    # request.GET
    # request.POST
    ro = {}
    os = request
    for f in dir(os):
        if not f.startswith('_'):
            ro[f] = getattr(os, f)

    sn = {}
    os = request.session
    for f in dir(os):
        if not f.startswith('_'):
            sn[f] = getattr(os, f)

    return HttpResponse(str({'request': ro, 'session': sn}))


def index3(request):
    # request.META
    #
    # 			'PATH_INFO': '/pac/r/test2',
    # 			'QUERY_STRING': 'a=q,b=d,c=x',

    return render(request, 'index.html', {'data': request.user})


def addSpidersBase(request):
    ret = 'no body!'
    # request.POST
    if request.method == 'POST':
        sbs = SpidersBaseSource()
        sbs.hash_id = hash(urls.getDT(2))
        sbs.service_type = request.POST.get('service_type', None)
        sbs.area = request.POST.get('area', None)
        sbs.province = request.POST.get('province', None)
        sbs.city = request.POST.get('city', None)
        sbs.tags = request.POST.get('tags', None)
        sbs.update_time = urls.getDT(2)
        sbs.url_source = request.POST.get('url_source', None)
        sbs.url_type = request.POST.get('url_type', None)
        sbs.resolve_type = request.POST.get('resolve_type', None)
        sbs.resolve_rule = request.POST.get('resolve_rule', None)
        sbs.resolve_source = request.POST.get('resolve_source', None)
        sbs.resolve_sources = request.POST.get('resolve_sources', None)
        sbs.resolve_next_page = request.POST.get('resolve_next_page', None)
        sbs.resolve_page_wait = request.POST.get('resolve_page_wait', None)
        # sbs.run_time = request.POST.get('run_time', None)
        sbs.run_count = request.POST.get('run_count', 0)
        sbs.content_page_rule = {}
        sbs.content_page_rule['resolve_type'] = request.POST.get('cresolve_type', None)
        sbs.content_page_rule['resolve_rule'] = request.POST.get('cresolve_rule', None)
        sbs.content_page_rule['resolve_source'] = request.POST.get('cresolve_source', None)
        sbs.bz1 = request.POST.get('bz1', None)
        sbs.bz2 = request.POST.get('bz2', None)
        print(sbs)
        print('sbs.save()')
        ret = sbs.save()
        print('return HttpResponse(str(ret))')
        ret = str(sbs.id)
    return HttpResponse(ret)


# 实现参数执行函数
def defun(this, fun, *a, **p):
    return eval(fun)(*a, **p) if p else eval(fun)(*a)


def pathRun(request):

    # 获取路径参数
    # request.META
    # 			'PATH_INFO': '/pac/r/s/...',
    # 			'QUERY_STRING': '{'a':'p','g':'y'}',
    # request.session.
    a = str(request.META['PATH_INFO'])
    a = a[a.find('//'):].strip('/').split('/')
    p = eval(request.META['QUERY_STRING'] if request.META['QUERY_STRING'] and str(a).find('}') > 0 else '{}')
    o = request
    sk = ''
    sv = {}
    if request.session.get(a[0]):
        sk = a[0]
        sv = o = pickle.loads(eval(request.session.get(a.pop(0))))
    ret = HttpResponse(str('no request!'))
    for y in a:
        y = str(y)
        if y.startswith('.'):
            o = getattr(o, y.lstrip('.'))
            ret = HttpResponse(str(o))
        elif y.endswith(')'):
            ret = o = defun(o, y.rstrip('()'), request, **p)
            request.session[sk] = str(pickle.dumps(sv))  # 重置操作后的对象
        else:
            o = o[y]
            ret = HttpResponse(str(o))

    return ret


class LP(object):

    test_list_page_threads = {'name': 'cc'}
    test_list_page_prints = []
    test_list_page_printsi = [0]

    def __init__(self):
        self.sdata = self.sdatao()

    def stop_test_list_page(self, request):
        ret = 'NO'
        if request.method == 'POST':
            tname = request.POST.get('tname', None)
            print('tname=' + tname)
            if tname and tname in self.test_list_page_threads.keys():
                # stop_thread(test_list_page_threads[tname])
                self.test_list_page_threads[tname].stop()
                ret = 'OK'
        return HttpResponse(str(ret))

    def read_print_test_list_page(self, request):
        ret = ''
        slen = len(self.sdata.test_list_page_prints)
        if slen > self.test_list_page_printsi[0]:
            ret = self.sdata.test_list_page_prints[self.test_list_page_printsi[0]:slen]
            self.test_list_page_printsi[0] = slen
        return HttpResponse(str(ret))

    def test_list_page(self, request):
        ret = 'no body!'
        # request.POST
        if request.method == 'POST':
            url_source = request.POST.get('url_source', None)
            resolve_page_wait = request.POST.get('resolve_page_wait', None)
            resolve_next_page = request.POST.get('resolve_next_page', None)
            resolve_type = request.POST.get('resolve_type', None)
            resolve_rule = request.POST.get('resolve_rule', None)
            resolve_sources = request.POST.get('resolve_sources', None)
            resolve_source = request.POST.get('resolve_source', None)
            self.test_list_page_printsi[0] = 0
            self.sdata.test_list_page_prints = []
            ret = self.MyThread(url_source, resolve_page_wait, resolve_next_page, resolve_type, resolve_rule,
                            resolve_sources, resolve_source, '', '', self.sdata)
            ret.start()

            self.test_list_page_threads[ret.getName()] = ret
            ret.join()  # 等待
            ret = str(ret.getName())
        return HttpResponse(ret)

    class MyThread(threading.Thread):
        def run(self):
            self._TS = SpiderBase.TS()
            self._TS.test_run(self.url_source, self.resolve_page_wait, self.resolve_next_page, self.resolve_type,
                              self.resolve_rule, self.resolve_sources, self.resolve_source, self.b_date, self.e_date,
                              self.s_data)

        def __init__(self, url_source, resolve_page_wait, resolve_next_page, resolve_type, resolve_rule,
                     resolve_sources, resolve_source, b_date, e_date, s_data):
            threading.Thread.__init__(self)
            self.url_source = url_source
            self.resolve_page_wait = resolve_page_wait
            self.resolve_next_page = resolve_next_page
            self.resolve_type = resolve_type
            self.resolve_rule = resolve_rule
            self.resolve_sources = resolve_sources
            self.resolve_source = resolve_source
            self.b_date = b_date
            self.e_date = e_date
            self.s_data = s_data

        def stop(self):
            self._TS.test_stop()

    class sdatao(object):
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


class IP(object):

    test_item_page_threads = {}
    test_item_page_prints = []
    test_item_page_printsi = [0]

    def __init__(self):
        self.sdata = self.sdatao()

    def stop_test_item_page(self, request):
        ret = 'NO'
        if request.method == 'POST':
            tname = request.POST.get('tname', None)
            print('tname=' + tname)
            if tname and tname in IP.test_item_page_threads.keys():
                # stop_thread(test_list_page_threads[tname])
                IP.test_item_page_threads[tname].stop()
                ret = 'OK'
        return HttpResponse(str(ret))

    def read_print_test_item_page(self, request):
        ret = ''
        slen = len(self.sdata.test_item_page_prints)
        if slen > IP.test_item_page_printsi[0]:
            ret = self.sdata.test_item_page_prints[IP.test_item_page_printsi[0]:slen]
            IP.test_item_page_printsi[0] = slen
        return HttpResponse(str(ret))

    def test_item_page(self, request):
        ret = 'no body!'
        # request.POST
        if request.method == 'POST':
            page_type = request.POST.get('cpage_type', None)
            resolve_pages = request.POST.get('curl_sources', None)
            resolve_type = request.POST.get('cresolve_type', None)
            resolve_rule = request.POST.get('cresolve_rule', None)
            resolve_source = request.POST.get('cresolve_source', None)
            IP.test_item_page_printsi[0] = 0
            self.sdata.test_item_page_prints = []
            ret = IP.MyThread(page_type, resolve_pages, resolve_type, resolve_rule, resolve_source, self.sdata)
            ret.start()
            IP.test_item_page_threads[ret.getName()] = ret
            ret.join()
            ret = ret.getName()
        return HttpResponse(ret)

    def show(self, request):
        # request.GET
        db = {'title': 'xxxxx', 'content': 'xxxxxxx'}
        if request.method == 'GET':
            url = request.META['QUERY_STRING']
            if url:
                url = url[str(url).find('http'):]
                db = self.sdata.db_url_content.get(url)
                # print('url=' + url)
                # print(spiders_data.sdata.db_url_content.keys())
        return render(request, 'core/showIP.html', db)

    class MyThread(threading.Thread):
        def run(self):
            self._T = SpiderBase.T()
            self._T.test_run(self.page_type, self.resolve_pages, self.resolve_type, self.resolve_rule,
                             self.resolve_source, self.sdata)

        def __init__(self, page_type, resolve_pages, resolve_type, resolve_rule, resolve_source, sdata):
            threading.Thread.__init__(self)
            self.page_type = page_type
            self.resolve_pages = resolve_pages
            self.resolve_type = resolve_type
            self.resolve_rule = resolve_rule
            self.resolve_source = resolve_source
            self.sdata = sdata

        def stop(self):
            self._T.test_stop()

    class sdatao(object):

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

