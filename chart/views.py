import pickle
from core import cache, util
from core.models import SpidersBaseSource
from django.shortcuts import render, HttpResponse
from TXSP import cache as tx_cache


def index(request):  # 控制台
    dbs = SpidersBaseSource.objects.all()
    print(len(dbs))
    request.session['dbs'] = str(pickle.dumps(dbs))

    ret = {'dbs': dbs}

    # 获取数据库统计数据
    try:
        ret.update(getdbchart(request, rest=False))
    except BaseException as e:
        print(e)

    # 获取内存统计数据
    try:
        cache_type = {'cache_pass': '有效','cache_time_error': '日期不符', 'cache_find_cf': '重复',
                     'cache_find_error': '错误', 'cache_Exception': '异常', 'cache_END': '时长'}
        cache_type_value = list(cache_type.values())
        ret.update({'cache_b': 'true', 'cache_type': cache_type, 'cache_type_value': cache_type_value})

        # 获取当前 session 中运行爬取的 key 值对应的对象数据
        dk = util.get_resolve_key(request)
        request.session[dk] = ''
        ret.update(getcachechart(request, rest=False))
    except BaseException as e:
        ret['cache_b'] = 'false'
        print(e)

    return render(request, 'core/manage/control.html', ret)


# 获取缓存统计数据
def getcachechart(request, rest=True):
    ret = {'cache_b': 'true'}
    uk = {}
    for i in pickle.loads(eval(request.session['dbs'])):
        uk[getattr(i, 'url_source')] = getattr(i, 'id')

    # 获取当前 session 中运行爬取的 key 值对应的对象数据
    dk = util.get_resolve_key(request)
    print('dk='+str(dk))
    if not (dk and dk in tx_cache.Data.txos.keys()):
        ret['cache_b'] = 'false'
        if request.session.get('ret_cache_buid'):
            ret.update(request.session.get('ret_cache_buid'))
        if request.session.get('ret_cache_key'):
            ret.update(request.session.get('ret_cache_key'))
        return HttpResponse(str(ret)) if rest else ret

    cachedb = tx_cache.Data.txos[dk].sdata.test_list_page_prints
    cachedbL = len(cachedb)
    # 获取当前 session 中的参数
    cache_test = request.session.get(dk)
    test_list_page_prints_i = 0
    cache_sesn = {}
    if cache_test:
        test_list_page_prints_i = cache_test['test_list_page_prints_i']
        cache_sesn = cache_test['cache_sesn']
        if test_list_page_prints_i == cachedbL and len(tx_cache.Data.txos[dk].sdata.test_list_page_threads) == 0:
            ret['cache_b'] = 'end'
            request.session['test_run_buid'] = None
            if request.session.get('ret_cache_buid'):
                ret.update(request.session.get('ret_cache_buid'))
            if request.session.get('ret_cache_key'):
                ret.update(request.session.get('ret_cache_key'))
            return HttpResponse(str(ret)) if rest else ret
    print('test_list_page_prints_i[%d] < cachedbL[%d]' % (test_list_page_prints_i, cachedbL))
    while test_list_page_prints_i < cachedbL:
        pstr = str(cachedb[test_list_page_prints_i])
        test_list_page_prints_i += 1
        # 统计页面爬取数据  '===this page Count=%d, time_error=%d, find_cf=%d, find_error=%d, Exception=%d, BY_URL=%s,==='
        if pstr.startswith("===this page Count="):
            # print('pstr='+pstr)
            BY_URL = util.get_log_key_value(pstr, 'BY_URL')
            if uk[BY_URL] not in cache_sesn.keys():
                cache_sesn[uk[BY_URL]] = {}
            if 'Count' in cache_sesn[uk[BY_URL]].keys():
                # print(cache_sesn[uk[BY_URL]])
                cache_sesn[uk[BY_URL]]['Count'] += int(util.get_log_key_value(pstr, 'Count'))
                cache_sesn[uk[BY_URL]]['Exception'] += int(util.get_log_key_value(pstr, 'Exception'))
                cache_sesn[uk[BY_URL]]['find_error'] += int(util.get_log_key_value(pstr, 'find_error'))
                cache_sesn[uk[BY_URL]]['find_cf'] += int(util.get_log_key_value(pstr, 'find_cf'))
                cache_sesn[uk[BY_URL]]['time_error'] += int(util.get_log_key_value(pstr, 'time_error'))
                cache_sesn[uk[BY_URL]]['pass'] = cache_sesn[uk[BY_URL]]['Count'] - cache_sesn[uk[BY_URL]]['Exception'] - \
                                                 cache_sesn[uk[BY_URL]]['find_error'] - cache_sesn[uk[BY_URL]]['find_cf'] - \
                                                 cache_sesn[uk[BY_URL]]['time_error']
                # print(cache_sesn[uk[BY_URL]])
            else:
                cache_sesn[uk[BY_URL]]['Count'] = int(util.get_log_key_value(pstr, 'Count'))
                cache_sesn[uk[BY_URL]]['Exception'] = int(util.get_log_key_value(pstr, 'Exception'))
                cache_sesn[uk[BY_URL]]['find_error'] = int(util.get_log_key_value(pstr, 'find_error'))
                cache_sesn[uk[BY_URL]]['find_cf'] = int(util.get_log_key_value(pstr, 'find_cf'))
                cache_sesn[uk[BY_URL]]['time_error'] = int(util.get_log_key_value(pstr, 'time_error'))
                cache_sesn[uk[BY_URL]]['pass'] = cache_sesn[uk[BY_URL]]['Count'] - cache_sesn[uk[BY_URL]]['Exception'] - \
                                                 cache_sesn[uk[BY_URL]]['find_error'] - cache_sesn[uk[BY_URL]]['find_cf'] - \
                                                 cache_sesn[uk[BY_URL]]['time_error']
            # print('find:%s' % cache_sesn[uk[BY_URL]])
        # 统计页面爬取时间  "##########END=%s, TS.processRequest=%s,##########"
        elif pstr.startswith("##########END=") and pstr.find('TS.processRequest=') > 0:
            # print('pstr='+pstr)
            BY_URL = util.get_log_key_value(pstr, 'processRequest')
            if uk[BY_URL] not in cache_sesn.keys():
                cache_sesn[uk[BY_URL]] = {}
            if 'END' in cache_sesn[uk[BY_URL]].keys():
                cache_sesn[uk[BY_URL]]['END'] += float(util.get_log_key_value(pstr, 'END'))
            else:
                cache_sesn[uk[BY_URL]]['END'] = float(util.get_log_key_value(pstr, 'END'))
            # print('find:%s' % cache_sesn[uk[BY_URL]])
        elif pstr.startswith("test_run_buid start"):
            # test_run_buid start:MyThread:Thread-3 [3/4] TO url_source=http://www.zzzyjy.cn/019/019001/019001001/secondPage.html
            nu = int(pstr[pstr.find('[') + 1:pstr.find('/')])
            co = int(pstr[pstr.find('/') + 1:pstr.find(']')])
            sum = request.session.get('test_run_buid')
            if not sum:
                sum = [0] * co
            sum[nu-1] = 1  # 表示已开始
            BY_URL = pstr[pstr.find('url_source=') + len('url_source='):]
            request.session['test_run_buid'] = sum
            pass
        elif pstr.startswith("test_run_buid stop"):
            # test_run_buid stop:MyThread:Thread-3 [3/4] TO url_source=http://www.zzzyjy.cn/019/019001/019001001/secondPage.html
            BY_URL = pstr[pstr.find('url_source=') + len('url_source='):]
            request.session['test_run_buid'][int(pstr[pstr.find('[') + 1:pstr.find('/')])-1] = 2  # 表示已结束
            pass
        # print('test_list_page_prints_i[%d] < cachedbL[%d]' % (test_list_page_prints_i, cachedbL))

    request.session[dk] = {'cache_sesn': cache_sesn, 'test_list_page_prints_i': test_list_page_prints_i}
    # print('request.session[dk]:%s' % request.session[dk])

    # 小图 1
    test_run_buid = request.session.get('test_run_buid')
    if not test_run_buid:
        test_run_buid = []
    cache_buid = []
    cache_buid.append({'name': '待爬取', 'value': test_run_buid.count(0)})
    cache_buid.append({'name': '爬取中', 'value': test_run_buid.count(1)})
    cache_buid.append({'name': '已爬取', 'value': test_run_buid.count(2)})
    request.session['ret_cache_buid'] = {'cache_buid': cache_buid, 'cache_buid_name': util.find_p1(cache_buid, 'name')}
    ret.update(request.session.get('ret_cache_buid'))

    # 小图 2
    cache_sesn_values = list(cache_sesn.values())
    cache_pass = []
    cache_time_error = []
    cache_find_cf = []
    cache_find_error = []
    cache_Exception = []
    cache_END = []
    for csv in cache_sesn_values:
        cache_pass.append(csv['pass'] if 'pass' in csv.keys() else 0)
        cache_time_error.append(csv['time_error'] if 'time_error' in csv.keys() else 0)
        cache_find_cf.append(csv['find_cf'] if 'find_cf' in csv.keys() else 0)
        cache_find_error.append(csv['find_error'] if 'find_error' in csv.keys() else 0)
        cache_Exception.append(csv['Exception'] if 'Exception' in csv.keys() else 0)
        cache_END.append(csv['END'] if 'END' in csv.keys() else 0)

    request.session['ret_cache_key'] = {'cache_key': list(cache_sesn.keys()),
                'cache_pass': cache_pass,
                'cache_time_error': cache_time_error,
                'cache_find_cf': cache_find_cf,
                'cache_find_error': cache_find_error,
                'cache_Exception': cache_Exception,
                'cache_END': cache_END}
    ret.update(request.session.get('ret_cache_key'))
    return HttpResponse(str(ret)) if rest else ret


# 获取数据库统计数据
def getdbchart(request, rest=True, dbs={}):
    ret = {}
    if not dbs:
        # dbs = pickle.loads(eval(request.session['dbs']))
        dbs = SpidersBaseSource.objects.all()
    # 数据状态
    # print(util.find_p1(dbs, 'url_type'))
    db_url_type = []
    db_url_type.append({'name': '执行失败', 'value': len(util.find_p(dbs, url_type='-2'))})
    db_url_type.append({'name': '已禁用', 'value': len(util.find_p(dbs, url_type='-1'))})
    db_url_type.append({'name': '已删除', 'value': len(util.find_p(dbs, url_type='0'))})
    db_url_type.append({'name': '待启用', 'value': len(util.find_p(dbs, url_type='1'))})
    db_url_type.append({'name': '执行中', 'value': len(util.find_p(dbs, url_type='2'))})
    db_url_type.append({'name': '测试', 'value': len(util.find_p(dbs, url_type='3'))})
    # print(db_url_type)
    ret.update({'db_url_type': db_url_type, 'db_url_type_name': util.find_p1(db_url_type, 'name'), 'db_url_type_value': util.find_p1(db_url_type, 'value')})

    # 业务类型
    db_service_type_name = util.find_p1(dbs, 'service_type')
    db_service_type = []
    db_service_type_value = []
    for stname in db_service_type_name:
        value = len(util.find_p(dbs, service_type=stname))
        db_service_type_value.append(value)
        db_service_type.append({'name': stname, 'value': value})
    # print(db_service_type)
    ret.update({'db_service_type': db_service_type, 'db_service_type_name': db_service_type_name, 'db_service_type_value': db_service_type_value})

    # 所属城市
    db_city_name = util.find_p1(dbs, 'city')
    db_city = []
    db_city_value = []
    for stname in db_city_name:
        value = len(util.find_p(dbs, city=stname))
        db_city_value.append(value)
        db_city.append({'name': stname, 'value': value})
    # print(db_city)
    ret.update({'db_city': db_city, 'db_city_name': db_city_name, 'db_city_value': db_city_value})

    # 所属区域
    db_area_name = util.find_p1(dbs, 'area')
    db_area = []
    db_area_value = []
    for stname in db_area_name:
        value = len(util.find_p(dbs, area=stname))
        db_area_value.append(value)
        db_area.append({'name': stname, 'value': value})
    # print(db_area)
    ret.update({'db_area': db_area, 'db_area_name': db_area_name, 'db_area_value': db_area_value})

    # 所属省份
    db_province_name = util.find_p1(dbs, 'province')
    db_province = []
    db_province_value = []
    for stname in db_province_name:
        value = len(util.find_p(dbs, province=stname))
        db_province_value.append(value)
        db_province.append({'name': stname, 'value': value})
    # print('db_province=')
    # print(db_province)
    ret.update({'db_province': db_province, 'db_province_name': db_province_name, 'db_province_value': db_province_value})
    return HttpResponse(str(ret)) if rest else ret


# 实现参数执行函数
def defun(this, fun, *a, **p):
    return eval(fun)(*a, **p) if p else eval(fun)(*a)


# url 动态调用对应接收函数
def rest(request):

    # 获取路径参数
    # request.META
    # 			'PATH_INFO': '/pac/chart/:/...',
    # 			'QUERY_STRING': '{'a':'p','g':'y'}',
    # request.session.
    # print('pathRun')
    a = str(request.META['PATH_INFO'])
    # print('PATH_INFO a='+a)
    a = a[a.find(':/')+1:].strip('/').split('/')
    # print(' a='+str(a))
    p = eval(request.META['QUERY_STRING'] if request.META['QUERY_STRING'] and str(request.META['QUERY_STRING']).find('}') > 0 else '{}')
    # print('p='+str(p))
    o = request
    # print('o='+str(o))
    sk = ''
    sv = {}
    # if request.session.get(a[0]):
    #     sk = a.pop(0)
    #     sv = request.session.get(sk)
    #     sv = o = pickle.loads(eval(sv))
    # elif a[0] == 'session':
    #     o = request.session
    #     sk = a.pop(0)
    if a[0] == 'session':
        o = request.session
        sk = a.pop(0)
        print('sk:%s sv:%s' % (sk, sv))
    elif request.session.session_key in cache.Data.LPs.keys():
        if a[0] == 'LP':
            sk = a.pop(0)
            sv = o = cache.Data.LPs.get(request.session.session_key)
            print('sk:%s sv:%s' % (sk, sv))
        elif a[0] == 'IP':
            sk = a.pop(0)
            sv = o = cache.Data.IPs.get(request.session.session_key)
            print('sk:%s sv:%s' % (sk, sv))
    print('session_key:%s keys:%s' % (request.session.session_key, list(cache.Data.LPs.keys())))
    ret = HttpResponse(str('no request!'))
    # print('ret')
    try:
        for y in a:
            y = str(y)
            # print('o=' + str(o))
            # print('y=' + y)
            if y.startswith('.'):
                o = getattr(o, y.lstrip('.'))
                ret = HttpResponse(str(o))
            elif y.endswith(')'):
                ret = o = defun(o, y.rstrip('()'), request, **p)
                # request.session[sk] = str(pickle.dumps(sv))  # 重置操作后的对象
                # print('request.session[sk]=' + str(request.session[sk]))
            else:
                try:
                    o = o[y]
                    ret = HttpResponse(str(o))
                except BaseException as e:
                    ret = HttpResponse(str('url error!'+y))
                    break
    except IOError as e:
        print('pathRun e:%s' % e)
    return ret
