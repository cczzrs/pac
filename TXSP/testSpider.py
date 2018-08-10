# coding=utf-8
import time
import threading
from dateutil import parser
from lxml import etree
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from django.shortcuts import render, HttpResponse
from concurrent.futures import ThreadPoolExecutor
from core import util, models
from TXSP import testSpider, cache, settings as sets


class TS(object):

    def processRequest(self, URL_TO, dbo, driver):
        self.printT("##########TS.processRequest##########")

        contentPage = 1
        contentCount = 0
        DB_URLS = []
        THIS_URLS = {}

        try:
            """ 
            [
                {"wait": '//div[@class="right_left"]'},
                {"next": '//input[@value="GO"]'},
                {"trs": [['//div[@class="right_left"]//table[2]//tr']]},
                {"tr": {"news_title": [['//td[@height="22"]//a/text()']],
                        "url_source": [['//td[@height="22"]//a/@href']],
                        "news_date": [['//td[@align="center"]//a/text()']]}}
            ]
            """
            dbo_wait = eval(dbo[0])
            dbo_next = eval(dbo[1])
            dbo_sources = eval(dbo[2])
            dbo_source = eval(dbo[3])

            wait = WebDriverWait(driver, timeout=sets.WEBDRIVERWAIT_TIMEOUT)
            wait.until(EC.visibility_of_element_located((By.XPATH, dbo_wait["wait"])))  # 等待渲染数据
            self.printT('driver.page_source=' + driver.page_source.replace('\n', ''))

            while self._runing and self._run_count > 0:
                self._run_count -= 1
                # 下一页
                lbs = []
                for tris in dbo_sources['trs']:
                    lbsbef = [etree.HTML(driver.page_source)]
                    for ti in tris:
                        lbsbe = []
                        for lbf in lbsbef:
                            # driver.find_elements_by_xpath("XPATH").extract()
                            lbsbe += lbf.xpath(str(ti))
                        lbsbef = lbsbe
                    lbs += lbsbef

                lbi = 0
                while lbi < len(lbs):
                    lbs[lbi] = str(etree.tostring(lbs[lbi], encoding='utf-8'), 'utf-8')
                    lbi += 1
                if lbi == 0:
                    continue
                self.printT('lbs=' + str(lbs))

                find_error = 0  # 重复或丢弃的数据数
                time_error = 0  # 数据时间不符合的数据数
                time_error_b = False  # 按顺序 判断时间数据
                error_t = 0
                find_cf = 0
                dbo_st = dbo_source['tr']
                for ld in lbs:
                    contentCount += 1
                    self.printT('###########' + str(contentCount) + '###########' + ld.replace('\n', ''))
                    ldo = {}
                    ld = etree.HTML(ld)
                    try:
                        for dtk in dbo_st.keys():
                            dtv = dbo_st.get(dtk)
                            # {"news_title": ['//td[@height="22"]//a/text()']}
                            ldo[dtk] = []
                            lb_f_ef = {}
                            for tr_is in dtv:
                                ld_ed = [ld]
                                for ti in tr_is:
                                    lbs_be = []
                                    for lb_f in ld_ed:
                                        lb_f_ef = lb_f
                                        lbs_be += lb_f.xpath(ti)
                                    ld_ed = lbs_be
                                if ld_ed and ld_ed[0] == '#':
                                    ti = str(tr_is[len(tr_is) - 1])
                                    ld_ed = lb_f_ef.xpath(ti[:ti.rfind('@')] + "@onclick")
                                ldo[dtk] += ld_ed
                            if len(ldo[dtk]) > 0:
                                ldo[dtk] = ''.join(ldo[dtk])
                            else:
                                ldo[dtk] = ''
                    except BaseException as e:
                        error_t += 1
                        self.printT('BaseException error_t=' + str(error_t) + ' by ' + dtk + ' \te:' + str(e))
                        continue

                    if not ldo['news_title'] or not ldo['url_source'] or not ldo['news_date']:  # 剔除垃圾数据
                        find_error += 1
                        self.printT('find_error=' + str(find_error))
                        continue

                    ldo['news_date'] = util.FPDate(ldo['news_date'])
                    if not ldo['news_date'] or ldo['news_date'] == '':
                        time_error += 1
                        print('time_error=' + str(time_error))
                        continue
                    n_date = util.FPDate(ldo['news_date'], 'date')
                    # print('self._com_date='+ str(self._com_date))
                    # print('self._b_date='+ str(self._b_date))
                    # print('self._e_date='+ str(self._e_date))
                    # print('n_date='+ str(n_date))
                    if self._com_date:
                        if (self._e_date - n_date).days >= 0 and (n_date - self._b_date).days >= 0:  # 时间范围限制
                            time_error_b = True
                            pass
                        else:
                            time_error += 1
                            self.printT('time_error=' + str(time_error))
                            continue

                    ldo['url_source'] = util.paseURL(URL_TO, ldo['url_source'])
                    if (ldo['url_source'] in DB_URLS) or (ldo['url_source'] in THIS_URLS.keys()):  # 判断是否已有该 url 数据
                        find_cf += 1
                        self.printT('find_cf=' + str(find_cf))
                    else:
                        THIS_URLS[ldo['url_source']] = ldo  # 添加到结果集

                    self.printT('ldo=' + str(ldo))

                self.printT('===this page Count=%d, time_error=%d, find_cf=%d, find_error=%d, Exception=%d==='
                            % (len(lbs), time_error, error_t, find_error, find_cf))
                if len(lbs) == error_t + find_error + find_cf:
                    self.printT('!!!!!!!!!!find all data over!!!!!!!!!!')
                    break
                if not self._runing or self._run_count < 1:  # 不满足循环条件不进行下一页操作
                    self.printT('self._runing and self._run_count' + str((self._runing, self._run_count)))
                    break
                if time_error_b and time_error > 0:  # 按时间顺序判断，如果有有效数据后，又没有有效数据了，则表示后续的数据时间都不在有效时间范围内
                    self.printT('time_error_b and time_error' + str((time_error_b, time_error)))
                    break
                if len(lbs) == time_error + error_t + find_error + find_cf and n_date and (
                        self._b_date - n_date).days > 0:  # 按时间顺序判断，如果整页数据都不匹配，则查看此页最后一条时间是否在时间范围之前
                    self.printT('len(lbs) == time_error and (self._b_date - n_date).days > 0')
                    break

                try:
                    wait.until(EC.visibility_of_element_located(
                        (By.XPATH, dbo_next['next']))).click()  # 等待渲染后点击下一页，没有下一页等待超时退出
                    contentPage += 1
                    self.printT('###########next' + str(contentPage) + '##########')

                    time.sleep(1.200)  # 等待 1.2 秒

                    wait.until(EC.visibility_of_element_located((By.XPATH, dbo_wait['wait'])))  # 等待渲染数据
                    self.printT('###########next data##########')

                except BaseException as e:
                    self.printT('###########data over########## e=' + str(e))
                    break

        except BaseException as e:
            self._runing = False
            self._e = e
            self.printT('processRequest ERROR e=' + str(e))
        self.printT('contentPage=' + str(contentPage))
        self.printT('contentCount=' + str(contentCount))
        if len(THIS_URLS) > 0:
            self._s_data.dbo_urls[URL_TO] = list(THIS_URLS.values())
        self.printT('self._s_data.dbo_urls[URL_TO]=' + str(len(self._s_data.dbo_urls)))
        return THIS_URLS

    def test_run_buid(url, pw, pn, pt, pg, prs, pr, b_date, e_date, s_data, to_log):
        print(to_log)
        TS().test_run(url, pw, pn, pt, pg, prs, pr, b_date, e_date, s_data)

    def test_run(self, url, pw, pn, pt, pg, prs, pr, b_date, e_date, s_data):
        if b_date == '' and e_date == '':
            self._com_date = False
        else:
            self._com_date = True
            self._b_date = parser.parse(b_date if b_date != '' else '2000-1-1')  # 默认开始时间 - '2000-1-1'
            self._e_date = parser.parse(e_date if e_date != '' else util.getDT())  # 默认结束时间 - 今天
        try:
            self._s_data = s_data
            self._run_count = s_data.run_count
            self._runing = True
            dbo = [pw, pn, prs, pr]

            options = Options()
            if not sets.EXECUTABLE_RUN_SHOW:
                options.add_argument('-headless')  # 无头参数
                options.add_argument('--no-sandbox')  # 禁用某个功能，该错误测了两天，颤毛啊！。（原因是运行Chrome浏览器报错，火狐不行）
                # options.add_argument('--disable-dev-shm-usage')
            driver = Chrome(executable_path=sets.EXECUTABLE_PATH, chrome_options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
            driver.set_script_timeout(sets.WEBDRIVERWAIT_TIMEOUT)
            driver.get(url)  # 加载

            retss = self.processRequest(url, dbo, driver)  # 执行

            driver.quit()
            print('driver.quit() end')
            if not self._runing:
                # self._s_data.dbo_urls_b = False  # 暂不标记为 全局数据无效
                self._s_data.up_dbo_error_urls[url] = self._e  # 异常数据 url 个更新状态到数据
            # self.printT('processRequest(url, dbo, driver) ed')
            self.printT('有效总数据：' + str(len(retss)))
            for r in retss:
                self.printT(r+'='+str(retss.get(r)))
            self.printT(url + '_end')  # 打印结束
        except BaseException as e:
            # self._s_data.dbo_urls_b = False  # 暂不标记为 全局数据无效
            self._e = e
            self._s_data.up_dbo_error_urls[url] = self._e  # 异常数据 url 个更新状态到数据
            self.printT('test_run ERROR e='+str(e))
            driver.quit()
            print('driver.quit() end')

    def test_stop(self):
        self._runing = False

    def printT(self, ps):
        self._s_data.test_list_page_prints.append(ps)
        if sets.PRINT_LOG:
            print(">>>>>>>>>>>" + str(ps))


class TX(object):

    def stop_test_list_page(self, request):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('!!!!!!!!!!stop_test_list_page key='+str(self.sdata.dbo_resolve_key)+'!')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        self.sdata.dbo_urls_b = False
        for tk in self.sdata.test_list_page_threads.keys():
            self.sdata.test_list_page_threads[tk].stop()

    def up_test_list_dbo(self):
        du_len = len(self.sdata.dbo_urls)
        print('up_test_list_dbo dulen='+str(du_len))
        if self.sdata.dbo_urls_b:
            if du_len > 0:  # 把数据更新到 内存 和 数据库
                if self.sdata.dbo_resolve_key in cache.Data.db_pac.keys():
                    cache.Data.db_pac.get(self.sdata.dbo_resolve_key).update(self.sdata.dbo_urls.copy())
                else:
                    cache.Data.db_pac.update({self.sdata.dbo_resolve_key: self.sdata.dbo_urls.copy()})
                self.sdata.dbo_urls.clear()
        else:
            if self.sdata.dbo_resolve_key in cache.Data.db_pac.keys():
                print('cache.Data.db_pac.pop(self.sdata.dbo_resolve_key) '+str(self.sdata.dbo_resolve_key))
                cache.Data.db_pac.pop(self.sdata.dbo_resolve_key)

        # up_dbo_error_urls
        du_len = len(self.sdata.up_dbo_error_urls)
        print('up_dbo_error_urls dulen='+str(du_len))
        if du_len > 0:  # 把数据更新到 内存 和 数据库
            # 更新到数据库
            pass

        pass

    def print_execl_test_list_page(self, request):
        # self.sdata.dbo_urls  # {url, [dbo]}
        dboss = []
        dboss.append(['网站根目录', '更新标题', '更新地址（双击访问）', '更新时间'])
        for uk in self.sdata.dbo_urls:
            for dbo in self.sdata.dbo_urls.get(uk):
                row = []
                row.append(uk)
                for dbok in dbo:
                    # row.append(dbok)
                    row.append(str(dbo.get(dbok)).strip())
                dboss.append(row)
        print(dboss)
        down_url = sets.DOWN_URL + 'pac_excel' + util.getDT() + '_' + str(time.time())[-3:] + '.xls'
        down_url = util.biuderEXECL(dboss, down_url)  # [[]]
        # return HttpResponse(str(self.sdata.dbo_urls))
        return render(request, 'index1.html', {'down_url': down_url[down_url.find('/pac_excel'):], 'data': self.sdata.dbo_urls})

    def test_list_page_runing(self, request, resolve_key):

        # request.POST
        if request.method == 'POST':
            service_type = request.POST.get('service_type', '对外招标')
            tags = request.POST.get('tags', 'tt')
            b_date = request.POST.get('b_date', util.getDT())  # '2018-7-16'
            e_date = request.POST.get('e_date', util.getDT())

            # base_sources = request.POST.get('base_sources', [])  # 指定网站

            b_date = util.getDT() if b_date == '' else b_date
            e_date = util.getDT() if e_date == '' else e_date

            # if (not self.sdata.db_dbo) or len(self.sdata.db_dbo) < 1:
            #    self.sdata.db_dbo = SpidersBaseSource.get_SpidersBaseSource_by_resolve_key(resolve_key)
            self.sdata.dbo_resolve_key = resolve_key  # str((service_type, b_date, e_date))
            self.sdata.dbo_urls = {}
            print('self.MyThread().start() '+str(self.sdata.dbo_resolve_key))
            ret = self.MyThread(self.sdata.db_dbo, b_date, e_date, self)

            ret.start()
            self.sdata.test_list_page_threads[ret.getName()] = ret
            print('self.MyThread().start().getName() '+str(ret.getName()))
            ret.join()

    class MyThread(threading.Thread):
        def run(self):
            SName = self.getName()
            print('run MyThread:'+str())
            try:
                self.threadpooles = ThreadPoolExecutor(sets.TESK_THREAD_POOL_EXECUTOR_LEN)  # 创建线程池
                with self.threadpooles:
                    sums = len(self.dbos)
                    count = 0
                    for dbo in self.dbos:
                        dbo = eval(str(dbo))
                        count += 1
                        to_log = 'MyThread:%s [%s/%s] TO url_source=%s' % (SName, count, sums, dbo['url_source'])
                        self.threadpooles.submit(testSpider.TS.test_run_buid,
                                                 dbo['url_source'], dbo['resolve_page_wait'],
                                                 dbo['resolve_next_page'], dbo['resolve_type'],
                                                 dbo['resolve_rule'], dbo['resolve_sources'],
                                                 dbo['resolve_source'], self.b_date, self.e_date, self.s_data, to_log)

            except BaseException as e:
                self.s_data.dbo_urls_b = False
                print("MyThread:%s ERROR:%s" % (SName, str(e)))

            self.baseo.up_test_list_dbo()
            print("MyThread:%s self.baseo.up_test_list_dbo()" % SName)

            self.s_data.test_list_page_threads.pop(self.getName())
            print("MyThread:%s over MyThread test_list_page_threads.pop(self.getName()):%s " % (SName, self.getName()))

        def __init__(self, dbos, b_date, e_date, baseo):
            threading.Thread.__init__(self)
            self.dbos = dbos
            self.b_date = b_date
            self.e_date = e_date
            self.baseo = baseo
            self.s_data = baseo.sdata

        def stop(self):
            self.s_data.dbo_urls_b = False
            print("self.s_data.dbo_urls_b = False")
            with self.threadpooles as executor:
                executor.shutdown(False)

            self.baseo.up_test_list_dbo()
            print("self.baseo.up_test_list_dbo()")

