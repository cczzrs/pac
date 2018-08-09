from django.shortcuts import render, HttpResponse
import settings
from dateutil import parser
from core import util
from core.models import SpidersBaseSource
from . import testSpider, cache
from concurrent.futures import ThreadPoolExecutor


TTPE = ThreadPoolExecutor(settings.TESKS_THREAD_POOL_EXECUTOR_LEN)  # 执行爬虫任务线程池


def get_resolve_key(request):  # 提取参数规则 key
    if request.method == 'GET':
        resolve_key = request.GET.get('resolve_key', '')
    elif request.method == 'POST':
        resolve_key = request.POST.get('resolve_key', '')
    return resolve_key


def index(request):  # 主页
    return render(request, 'TXSP/index.html')


def get_test_list_dbo(request):  # 获取爬取的数据
    return HttpResponse(str(cache.Data.db_pac.get(get_resolve_key(request))))


def get_test_is_runing(request):  # 获取爬虫状态
    ret = 'runed'
    resolve_key = get_resolve_key(request)
    if resolve_key in cache.Data.txos.keys():
        if cache.Data.txos[resolve_key]:
            if len(cache.Data.txos[resolve_key].sdata.test_list_page_threads) > 0:
                ret = 'runing'
            elif (resolve_key+'ed' not in cache.Data.txos.keys()) or (not cache.Data.txos[resolve_key + 'ed']):
                # cache.Data.txos[resolve_key] = None  # 暂不清空
                cache.Data.txos[resolve_key + 'ed'] = True  # 该标记为，结束的操作只执行一次
                if len(cache.Data.txos[resolve_key].sdata.up_dbo_error_urls) > 0:  # 判断是否有异常数据，有则更新到数据库
                    SpidersBaseSource.updateBy_RK_URLS_to_status(resolve_key, cache.Data.txos[resolve_key].sdata.up_dbo_error_urls)
                if resolve_key in cache.Data.db_pac.keys():  # 根据列表的网站倒序，并非所有数据
                    for urlk in cache.Data.db_pac[resolve_key]:
                        cache.Data.db_pac[resolve_key][urlk].sort(key=lambda s: parser.parse(s['news_date']), reverse=True)  # 数据按时间倒序
    return HttpResponse(ret)


def test_to_runing(request, resolve_key, db_dbo_new=None):  # 运行爬虫
    if not db_dbo_new:
        db_dbo_new = SpidersBaseSource.get_by_resolve_key(resolve_key)
        print('test_to_runing SpidersBaseSource.get_SpidersBaseSource_by_resolve_key(resolve_key)ed:'+str(len(db_dbo_new)))
    txo = testSpider.TX()
    txo.sdata = cache.sdatao()  # 初始化独立数据对象
    txo.sdata.db_dbo = db_dbo_new
    cache.Data.txos[resolve_key] = txo
    # txo.test_list_page_runing(request, resolve_key)
    cache.Data.db_pac[resolve_key] = {}  # 初始化 或者 清除老数据
    print('test_to_runing TTPE.submit(txo.test_list_page_runing, request, resolve_key)')
    TTPE.submit(txo.test_list_page_runing, request, resolve_key)


def test_list_page(request):  # 爬取数据
    resolve_key = 'error is no resolve_key!'
    # request.POST
    if request.method == 'POST':
        service_type = request.POST.get('service_type', '对外招标')
        rerun = request.POST.get('rerun', False)
        if rerun or rerun == 'true':
            rerun = True
        b_date = request.POST.get('b_date', util.getDT())  # '2018-7-16'
        e_date = request.POST.get('e_date', util.getDT())

        b_date = util.getDT() if b_date == '' else b_date
        e_date = util.getDT() if e_date == '' else e_date

        resolve_key = str((service_type, 'tt', b_date, e_date))  # 构建 resolve_key

        if (not rerun) and resolve_key in cache.Data.db_pac.keys():  # 判断是否已有数据，根据 resolve_key，并且数据库数据未有变化
            db_dbo_new = SpidersBaseSource.get_by_resolve_key(resolve_key)
            if len(db_dbo_new) != len(cache.Data.txos[resolve_key].sdata.db_dbo) or str(db_dbo_new) != str(cache.Data.txos[resolve_key].sdata.db_dbo):
                test_to_runing(request, resolve_key, db_dbo_new)  # 运行爬虫
        else:
            test_to_runing(request, resolve_key)  # 运行爬虫

    return HttpResponse(resolve_key)


def stop_test_list_page(request):  # 停止指定爬虫
    if cache.Data.txos[get_resolve_key(request)]:
        cache.Data.txos[get_resolve_key(request)].stop_test_list_page(request)
        return HttpResponse(str('OK'))
    else:
        return HttpResponse(str('OKED'))


def runingl_test():  # 当前运行的爬虫数量
    runingl = 0
    for txok in cache.Data.txos.keys():
        if cache.Data.txos[txok]:
            if len(cache.Data.txos[txok].sdata.test_list_page_threads) == 0:
                # cache.Data.txos[txok] = None  # 暂不清空
                pass
            else:
                runingl += 1
    return runingl


def clear_test(request):  # 当前爬虫数量总和，当前运行的爬虫数量
    return HttpResponse(set({'runs': len(cache.Data.txos), 'runing': runingl_test()}))

