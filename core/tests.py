import threading, pickle, json
from core import SpiderBase, cache
from django.shortcuts import render, HttpResponse


class pac_list_page(object):

    def __init__(self):
        self.test_list_page_threads = {}
        self.test_list_page_printsi = [0]

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


class pac_item_page(object):

    def __init__(self):
        self.test_item_page_threads = {}
        self.test_item_page_printsi = [0]

    def stop_test_item_page(self, request):
        ret = 'NO'
        if request.method == 'POST':
            tname = request.POST.get('tname', None)
            print('tname=' + tname)
            if tname and tname in self.test_item_page_threads.keys():
                # stop_thread(test_list_page_threads[tname])
                self.test_item_page_threads[tname].stop()
                ret = 'OK'
        return HttpResponse(str(ret))

    def read_print_test_item_page(self, request):
        ret = ''
        slen = len(self.sdata.test_item_page_prints)
        if slen > self.test_item_page_printsi[0]:
            ret = self.sdata.test_item_page_prints[self.test_item_page_printsi[0]:slen]
            self.test_item_page_printsi[0] = slen
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
            self.test_item_page_printsi[0] = 0
            self.sdata.test_item_page_prints = []
            ret = self.MyThread(page_type, resolve_pages, resolve_type, resolve_rule, resolve_source, self.sdata)
            ret.start()
            self.test_item_page_threads[ret.getName()] = ret
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
                # print('show url=%s db_url_content.keys=%s' % (url, self.sdata.db_url_content.keys()))
                # db = self.sdata.db_url_content.get(url)
                print('show url=%s cache.Data.db_url_content.keys=%s' % (url, cache.Data.db_url_content.keys()))
                db = cache.Data.db_url_content.get(url)
        return render(request, 'core/showIP.html', db)

    class MyThread(threading.Thread):
        def run(self):
            self._T = SpiderBase.T()
            self._T.test_run(self.page_type, self.resolve_pages, self.resolve_type, self.resolve_rule, self.resolve_source, self.sdata)
            cache.Data.db_url_content.update(self.sdata.db_url_content)

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
