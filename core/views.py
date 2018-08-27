import threading, pickle, json, time
from core import service, cache, util
from core.models import SpidersBaseSource
from django.shortcuts import render, HttpResponse


def index_mg(request):  # 管理首页
    dbs = SpidersBaseSource.tfilter()
    return render(request, 'core/manage/index.html', {'dbs': dbs})


def index_look(request):  # 查看
    tid = int(request.GET.get('tid'))
    dbi = SpidersBaseSource.get(id=tid)
    return render(request, 'core/index.html', {'dbi': dbi, 'look': True})


def index_edit(request):  # 编辑
    tid = int(request.GET.get('tid'))
    dbi = SpidersBaseSource.get(id=tid)
    return render(request, 'core/index.html', {'dbi': dbi, 'edit': True})


def index_del(request):  # 删除
    ret = 'no body!'
    status = '401'
    # request.POST
    if request.method == 'POST':
        tid = request.POST.get('tid', None)
        if tid:
            print('SpidersBaseSource.update()')
            update = {'url_type': '0'}
            print('index_del tid=%s, update=%s' % (tid, str(update)))
            ret = list(SpidersBaseSource.objects.filter(id=tid).update(**update))
            status = '200'
    return HttpResponse(str({'status': status, 'tid': ret}))


def index_qiy(request):  # 启用
    ret = 'no body!'
    status = '401'
    # request.POST
    if request.method == 'POST':
        tid = request.POST.get('tid', None)
        if tid:
            print('SpidersBaseSource.update()')
            update = {'url_type': '2'}
            print('index_del tid=%s, update=%s' % (tid, update))
            ret = list(SpidersBaseSource.objects.filter(id=tid).update(**update))
            status = '200'
    return HttpResponse(str({'status': status, 'tid': ret}))


def index_up(request):  # 更新
    ret = 'no body!'
    status = '401'
    # request.POST
    if request.method == 'POST':
        tid = request.POST.get('id', None)
        if tid:
            sbs = SpidersBaseSource.objects.get(id=tid)
            sbs.service_type = request.POST.get('service_type', None)
            sbs.area = request.POST.get('area', None)
            sbs.province = request.POST.get('province', None)
            sbs.city = request.POST.get('city', None)
            sbs.tags = request.POST.get('tags', None)
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
            print('sbs.update()')
            ret = sbs.save()
            ret = str(sbs.id)
            status = '200'
    return HttpResponse(str({'status': status, 'tid': ret}))


def index_db(request):  # 录数据页面
    if request.session.session_key not in cache.Data.LPs.keys():
        pac_list_page = service.pac_list_page()
        pac_item_page = service.pac_item_page()
        pac_list_page.sdata = pac_item_page.sdata = cache.sdatao()
        cache.Data.LPs[request.session.session_key] = pac_list_page
        cache.Data.IPs[request.session.session_key] = pac_item_page
        request.session['LP'] = str(pickle.dumps(pac_list_page))
        request.session['IP'] = str(pickle.dumps(pac_item_page))
    return render(request, 'core/index.html')


def test1(request):
    # request.GET
    # request.POST
    if request.session.session_key in cache.Data.LPs.keys():
        sv = o = cache.Data.LPs.get(request.session.session_key)
        print('session_key:%s sv:%s' % (request.session.session_key, sv))
        ret = HttpResponse(str(o.sdata.time))
    return ret


def test2(request):
    print('request.session.get='+request.session.get('LP'))
    if request.session.get('LP'):
        o = pickle.loads(eval(request.session.get('LP')))
        print('session_key:%s o:%s' % (request.session.session_key, o))
        ret = HttpResponse(str(o.sdata.time))
    return ret


def test(request):
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


def addSpidersBase(request):  # 添加
    ret = 'no body!'
    status = '401'
    # request.POST
    if request.method == 'POST':
        sbs = SpidersBaseSource()
        sbs.hash_id = hash(util.getDT(2))
        sbs.service_type = request.POST.get('service_type', None)
        sbs.area = request.POST.get('area', None)
        sbs.province = request.POST.get('province', None)
        sbs.city = request.POST.get('city', None)
        sbs.tags = request.POST.get('tags', None)
        sbs.update_time = util.getDT(2)
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
        status = '200'
    return HttpResponse({'status': status, 'tid': ret})


# 实现参数执行函数
def defun(this, fun, *a, **p):
    return eval(fun)(*a, **p) if p else eval(fun)(*a)


def pathRun(request):

    # 获取路径参数
    # request.META
    # 			'PATH_INFO': '/pac/r/s/:/...',
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
    print('session_key:%s keys:%s' % (request.session.session_key, cache.Data.LPs.keys()))
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
