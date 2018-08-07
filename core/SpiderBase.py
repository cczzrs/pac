# coding=utf-8
import os
import time
import json
import requests
import settings as set
from lxml import etree
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from dateutil import parser
from core import util


class TS(object):

    def processRequest(self, URL_TO, dbo):
        self.printT("##########TS.processRequest##########")

        contentPage = 1
        contentCount = 0
        DB_URLS = []
        THIS_URLS = {}

        options = Options()
        if not set.EXECUTABLE_RUN_SHOW:
            options.add_argument('-headless')  # 无头参数
        driver = Chrome(executable_path=set.EXECUTABLE_PATH, chrome_options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
        wait = WebDriverWait(driver, timeout=set.WEBDRIVERWAIT_TIMEOUT)

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
        dbo_wait = eval(dbo[0])  # {"wait": '//div[@class="right_left"]'}
        dbo_next = eval(dbo[1])  # {"next": '//div[@id="page_div"]//a[contains(text(), "下一页")]'}
        dbo_sources = eval(dbo[2])  # {"trs": [['//div[@class="right_left"]//table[2]//tr']]}
        dbo_source = eval(dbo[3])  # {"tr": {"news_title": [['//td[@height="22"]//a/text()']],
        #                                    "url_source": [['//td[@height="22"]//a/@href']],
        #                                    "news_date": [['//td[@align="center"]//a/text()']]}}

        try:
            # driver.set_script_timeout(15)
            driver.get(URL_TO)  # 加载

            wait.until(EC.visibility_of_element_located((By.XPATH, dbo_wait["wait"])))  # 等待渲染数据
            self.printT('driver.page_source=' + driver.page_source.replace('\n', ''))
        except BaseException as e:
            self._runing = False
            self.printT('driver.page_source e=' + str(e))

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
                                ti = str(tr_is[len(tr_is)-1])
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
                        print('time_error=' + str(time_error))
                        continue

                ldo['url_source'] = util.paseURL(URL_TO, ldo['url_source'])
                if (ldo['url_source'] in DB_URLS) or (ldo['url_source'] in THIS_URLS.keys()):  # 判断是否已有该 url 数据
                    find_cf += 1
                    self.printT('find_cf=' + str(find_cf))
                else:
                    THIS_URLS[ldo['url_source']] = ldo

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
            if len(lbs) == time_error + error_t + find_error + find_cf and n_date and (self._b_date - n_date).days > 0:  # 按时间顺序判断，如果整页数据都不匹配，则查看此页最后一条时间是否在时间范围之前
                self.printT('len(lbs) == time_error and (self._b_date - n_date).days > 0')
                break

            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, dbo_next['next']))).click()  # 等待渲染后点击下一页，没有下一页等待超时退出
                contentPage += 1
                self.printT('###########next' + str(contentPage) + '##########')

                time.sleep(1.200)  # 等待 1.2 秒

                wait.until(EC.visibility_of_element_located((By.XPATH, dbo_wait['wait'])))  # 等待渲染数据
                self.printT('###########next data##########')

            except BaseException as e:
                self.printT('###########data over########## e=' + str(e))
                break

        self.printT('contentPage=' + str(contentPage))
        self.printT('contentCount=' + str(contentCount))
        driver.quit()
        self.printT('driver.quit() end')
        self._s_data.dbo_urls[URL_TO] = list(THIS_URLS.values())
        self.printT('self._s_data.dbo_urls[URL_TO]='+str(len(self._s_data.dbo_urls)))
        return THIS_URLS

    def test_run(self, url, pw, pn, pt, pg, prs, pr, b_date, e_date, s_data):
        if b_date == '' and e_date == '':
            self._com_date = False
        else:
            self._com_date = True
            self._b_date = parser.parse(b_date if b_date != '' else '2000-1-1')  # 默认开始时间 - '2000-1-1'
            self._e_date = parser.parse(e_date if e_date != '' else util.getDT())  # 默认结束时间 - 今天

        self._s_data = s_data
        # self._run_count = s_data.run_count
        self._run_count = int(pt)
        self._runing = True
        dbo = [pw, pn, prs, pr]
        retss = self.processRequest(url, dbo)  # 执行
        # self.printT('processRequest(url, dbo) ed')  # 打印
        self.printT('有效总数据：' + str(len(retss)))  # 打印
        for r in retss:
            self.printT(r+'='+str(retss.get(r)))  # 打印
        self.printT(url + '_end')  # 打印结束

    def test_stop(self):
        self._runing = False

    def printT(self, ps):
        self._s_data.test_list_page_prints.append(ps)
        print(">>>>>>>>>>>" + str(ps))


class T(object):

    def processRequest(self, URL_TO, dbo):
        self.printT("##########T.processRequest##########")

        options = Options()
        if not set.EXECUTABLE_RUN_SHOW:
            options.add_argument('-headless')  # 无头参数
        driver = Chrome(executable_path=set.EXECUTABLE_PATH, chrome_options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
        wait = WebDriverWait(driver, timeout=set.WEBDRIVERWAIT_TIMEOUT)

        """ 
         [
            '1',
            'XPATH',
            '[[\'//*[@id="container"]/div/div/div[1]/div[2]/div/table/tbody/tr/td/table[1]/tbody/tr/td[2]/table[2]\']]'
         ]
        """
        dbo_type = dbo[0]  # '1'
        dbo_rule = dbo[1]  # 'XPATH'
        # dbo_source = json.loads(dbo[2])  # '[["//*[@id=\"container\"]/div/div/div[1]/div[2]/div/table/tbody/tr/td/table[1]/tbody/tr/td[2]/table[2]"]]'
        dbo_source = list(eval(dbo[2]))

        # driver.set_script_timeout(15)
        driver.get(URL_TO)  # 加载

        page = []
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, dbo_source[0][0])))  # 等待渲染数据
            # self.printT('driver.page_source=' + driver.page_source.replace('\n', ''))

            for tris in dbo_source:
                lbsbef = [etree.HTML(driver.page_source)]
                for ti in tris:
                    lbsbe = []
                    for lbf in lbsbef:
                        lbsbe += lbf.xpath(str(ti))
                    lbsbef = lbsbe
                page += lbsbef
            lbi = 0
            while lbi < len(page):
                page[lbi] = str(etree.tostring(page[lbi], encoding='utf-8'), 'utf-8')
                lbi += 1
            self.printT('page=' + str(page))

            if self._runing == False:
                return page
            page_content = ''.join(page)
            page_title = etree.HTML(driver.page_source).xpath('/html/head/title/text()')
            self._s_data.db_url_content[URL_TO] = {'title': page_title, 'content': page_content}
            self.printT('down=' + self.downIMG({'url': URL_TO, 'content': page_content}))
        except IOError as e:
            self.printT('!!!!!!!!!!find all data over!!!!!!!!!!')
        driver.quit()
        return page

    def downIMG(self, item):
        # 下载图片
        imgPath = set.WEB_DOWN_FILE_PATH  # 下载图片的保存路径
        downURLs = {}
        downURLsed = self._s_data.downURLs.keys()
        tHTML = etree.HTML(item['content'])

        for url in tHTML.xpath('//img/@src'):
            try:
                if url == '' or url.find('.') == -1 or url in downURLsed:
                    continue
                url = util.paseURL(item['url'], url)
                downURLs[url] = url.replace(url[0:url[8:].find('/') + 8], imgPath)
                downURLsed.append(url)
            except BaseException as e:
                continue
        for url in tHTML.xpath('//a/@href'):
            try:
                if url == '' or url == '#' or url.find('.') == -1 or url in downURLsed:
                    continue
                url = util.paseURL(item['url'], url)
                downURLs[url] = url.replace(url[0:url[8:].find('/') + 8], imgPath)
                downURLsed.append(url)
            except BaseException as e:
                continue

        if self._runing == False:
            return '[return]'
        self._s_data.downURLs.update(downURLs)
        self.printT('downURLs=' + str(len(downURLs)))
        ret = '0'
        if len(downURLs) > 0:
            ret = self.downLoadToFileByUrls(downURLs)
        return ret

    def downLoadToFileByUrls(self, urlsos):
        noi = 0
        # 未能正确获得网页 就进行异常处理
        for url in urlsos.keys():
            self.printT("文件下载:url:" + url)
            self.printT("文件储存:path:" + urlsos.get(url))
            try:
                imgPathTo = urlsos.get(url)
                if not os.path.isdir(imgPathTo[0:imgPathTo.rfind('/')]):
                    os.makedirs(imgPathTo[0:imgPathTo.rfind('/')])
                elif os.path.isfile(imgPathTo):
                    if set.WEB_DOWN_FILE_REDOWN:
                        os.remove(imgPathTo)
                    else:
                        self.printT('该文件已存在')
                        return '[return]'
                r = requests.get(url)
                r.raise_for_status()
                # 使用with语句可以不用自己手动关闭已经打开的文件流
                with open(imgPathTo, "wb") as f:  # 开始写文件，wb代表写二进制文件
                    f.write(r.content)
                    self.printT('下载完成')
            except BaseException as e:
                noi = noi + 1
                self.printT('未下载成功 e=' + str(e))
            if self._runing == False:
                return '[return]'
        ret = 1
        if noi > 0:
            ret = 2
            if noi > 1:
                ret = 3

        return str(ret)

    def test_run(self, py, urls, pt, pg, pr, s_data):
        self._s_data = s_data
        self._runing = True
        dbo = [pt, pg, pr]
        retss = []
        url = ''
        urls = json.loads(urls)
        for url in urls:
            if self._runing:
                self.printT(url + '_begin')
                retss += self.processRequest(url, dbo)  # 执行
                self.printT(url + '_over')  # 打印结束
            else:
                break
        # self.printT('processRequest(url, dbo) ed')  # 打印
        # for r in retss:
        # self.printT(str(r))  # 打印
        self.printT('有效总数据：' + str(len(retss)))  # 打印
        self.printT(url + '_end')  # 打印结束

    def test_stop(self):
        self._runing = False

    def printT(self, ps):
        self._s_data.test_item_page_prints.append(ps)
        print("item>>>>>>>>>>>" + str(ps))


