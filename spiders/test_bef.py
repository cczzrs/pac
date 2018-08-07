import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from spiders import spiders_data


class TS(object):

    def processRequest(self, URL_TO, dbo):
        self.printT("##########FMiddleware process_request##########")

        contentPage = 1
        contentCount = 0
        """
        http://land.dg.gov.cn/007330205/0403/gtjList.shtml
        """

        # URL_TO = 'http://land.dg.gov.cn/007330205/0403/gtjList.shtml'
        DB_URLS = []
        THIS_URLS = {}

        options = Options()
        # options.add_argument('-headless')  # 无头参数
        driver = Firefox(executable_path='geckodriver', firefox_options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径

        wait = WebDriverWait(driver, timeout=10)

        # SELECT hash_id, url_source, resolve_page_wait, resolve_next_page, resolve_type, resolve_rule, resolve_source

        """ {
                "trs": [
                    ["table", {
                        "width": "100%",
                        "border": "0",
                        "cellspacing": "0",
                        "cellpadding": "0"
                    }],
                    ["tr", {
                        "height": "20"
                    }, '']
                ],
                "tr": {
                    "news_title": [
                        ["td", {}, ''],
                        ["a", {
                            "target": "_blank"
                        }, "text"]
                    ],
                    "url_source": [
                        ["td", {}, ''],
                        ["a", {
                            "target": "_blank"
                        }, "href"]
                    ],
                    "news_date": [
                        ["td", {
                            "align": "right",
                            "width": "120"
                        }, "text"]
                    ]
                }
            }
        """
        dbo_wait = eval(dbo[0])  # {"XPATH": '//div[contains(@class, "list_div")]'}
        dbo_next = eval(dbo[1])  # {"XPATH": '//div[@id="page_div"]//a[contains(text(), "下一页")]'}
        dbo_source = eval(dbo[2])

        driver.get(URL_TO)  # 加载
        # driver.set_script_timeout(15)

        # 等待渲染数据
        if 'XPATH' in dbo_wait.keys():
            wait.until(EC.visibility_of_element_located((By.XPATH, dbo_wait["XPATH"])))  # 等待渲染数据
        else:
            wait.until(EC.visibility_of_element_located((By.XPATH, dbo_wait["XPATH"])))  # 等待渲染数据

        self.printT('driver.page_source=' + driver.page_source.replace('\n', ''))

        while True:
            # 下一页

            bs = BeautifulSoup(driver.page_source, 'lxml')
            lbs = []
            lbsbef = []
            lbsbef.append(bs)
            for tris in dbo_source['trs']:
                lbs = []
                for lb in lbsbef:
                    if len(tris) > 2 and tris[2] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        lb.append(lb.find_all(tris[0], attrs=tris[1])[int(tris[2])-1])
                    else:
                        lbs = lbs + lb.find_all(tris[0], attrs=tris[1])
                lbsbef = lbs

            findCF = 0  # 重复或丢弃的数据数
            dbo_st = dbo_source['tr']
            for ld in lbs:
                contentCount += 1
                self.printT('###########' + str(contentCount) + '###########' + str(ld).replace('\n', ''))

                ldo = {}
                errori = 0
                # news_title:[td,{'align':'right'},test]
                for dtk in dbo_st.keys():
                    dsts = dbo_st.get(dtk)
                    lded = []
                    lded.append(ld)
                    try:
                        for dst in dsts:
                            if len(dst) > 3:  # text=re.compile(dst[2])  regexp 表达式对象
                                if str(dst[2]) in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                                    lded[0] = lded[0].find_all(dst[0], text=re.compile(dst[3]), attrs=dst[1])
                                    if len(lded[0]):
                                        lded[0] = lded[0][int(dst[2])]
                                        if lded[0]:
                                            ldo[dtk] = lded[0].replace('\n', '')
                                elif str(dst[2]) == '*':
                                    ldo[dtk] = []
                                    for ldi in lded:
                                        ldo[dtk] = ldo[dtk] + ldi.find_all(dst[0], text=re.compile(dst[3]),
                                                                           attrs=dst[1])
                                    lded = ldo[dtk]
                                elif str(dst[2]) == '':
                                    lded[0] = lded[0].find(dst[0], text=re.compile(dst[3]), attrs=dst[1])
                                    if lded[0]:
                                        ldo[dtk] = lded[0]
                                elif str(dst[2]) == 'text':
                                    ldo[dtk] = lded[0].find(dst[0], text=re.compile(dst[3]), attrs=dst[1])
                                    if ldo[dtk] and ldo[dtk].text:
                                        ldo[dtk] = ldo[dtk].text.replace('\n', '')
                                else:
                                    if dst[0] == '':
                                        ldo[dtk] = lded[0]
                                    else:
                                        ldo[dtk] = lded[0].find(dst[0], text=re.compile(dst[3]), attrs=dst[1])
                                    if ldo[dtk] and ldo[dtk][dst[2]]:
                                        if ldo[dtk][dst[2]] == '#':
                                            ldo[dtk] = ldo[dtk]['onclick'].replace('\n', '')
                                        else:
                                            ldo[dtk] = ldo[dtk][dst[2]].replace('\n', '')
                            else:
                                if str(dst[2]) in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                                    lded[0] = lded[0].find_all(dst[0], attrs=dst[1])
                                    if len(lded[0]):
                                        lded[0] = lded[0][int(dst[2])]
                                        if lded[0]:
                                            ldo[dtk] = lded[0].replace('\n', '')
                                elif str(dst[2]) == '*':
                                    ldo[dtk] = []
                                    for ldi in lded:
                                        ldo[dtk] = ldo[dtk] + ldi.find_all(dst[0], attrs=dst[1])
                                    lded = ldo[dtk]
                                elif str(dst[2]) == '':
                                    ldo[dtk] = lded[0] = lded[0].find(dst[0], attrs=dst[1])
                                elif str(dst[2]) == 'text':
                                    ldo[dtk] = lded[0].find(dst[0], attrs=dst[1])
                                    if ldo[dtk] and ldo[dtk].text:
                                        ldo[dtk] = ldo[dtk].text.replace('\n', '')
                                else:
                                    if dst[0] == '':
                                        ldo[dtk] = lded[0]
                                    else:
                                        ldo[dtk] = lded[0].find(dst[0], attrs=dst[1])
                                    if ldo[dtk] and ldo[dtk][dst[2]]:
                                        if ldo[dtk][dst[2]] == '#':
                                            ldo[dtk] = ldo[dtk]['onclick'].replace('\n', '')
                                        else:
                                            ldo[dtk] = ldo[dtk][dst[2]].replace('\n', '')
                    except BaseException as e:
                        errori = errori + 1
                        self.printT('BaseException' + str(errori) + ' by ' + dtk + '\ne:' + str(e))
                        continue
                # 剔除垃圾数据
                if not ldo['news_title']:
                    findCF += 1
                    self.printT('findCF=' + str(findCF))
                    continue

                if errori == 0:
                    ldo['news_date'] = self.FPDate(ldo['news_date'])
                    ldo['url_source'] = self.paseURL(URL_TO, ldo['url_source'])
                    # 判断是否已有该 url 数据
                    if (ldo['url_source'] in DB_URLS) or (ldo['url_source'] in THIS_URLS.keys()):
                        findCF += 1
                        self.printT('findCF=' + str(findCF))
                    else:
                        THIS_URLS[ldo['url_source']] = ldo

                    ldo['news_date'] = self.FPDate(ldo['news_date'])

                self.printT('data item ldo=' + str(ldo))

            if len(lbs) == findCF:
                self.printT('!!!!!!!!!!findCF all data over!!!!!!!!!!')
                break
            self.printT('lds=' + str(lbs).replace('\n', ''))

            try:
                if 'XPATH' in dbo_next.keys():
                    tupleXPATH = (By.XPATH, dbo_next['XPATH'])
                    wait.until(EC.visibility_of_element_located(tupleXPATH)).click()  # 等待渲染后点击下一页，没有下一页等待超时退出
                else:
                    tupleXPATH = (By.XPATH, dbo_next['XPATH'])
                    wait.until(EC.visibility_of_element_located(tupleXPATH)).click()  # 等待渲染后点击下一页，没有下一页等待超时退出
                contentPage += 1
                self.printT('###########next' + str(contentPage) + '##########')

                # 等待 1.2 秒
                time.sleep(1.200)

                # 等待渲染数据
                if 'XPATH' in dbo_wait.keys():
                    wait.until(EC.visibility_of_element_located((By.XPATH, dbo_wait['XPATH'])))  # 等待渲染数据
                else:
                    wait.until(EC.visibility_of_element_located((By.XPATH, dbo_wait['XPATH'])))  # 等待渲染数据
                    self.printT('###########next data##########')

            except BaseException as e:
                self.printT('###########data over########## e=' + str(e))
                break

        self.printT('contentPage=' + str(contentPage))
        self.printT('contentCount=' + str(contentCount))
        driver.quit()

        return THIS_URLS

    def FPDate(dts):
        dts = str(dts).replace("\n", r"\n")
        # \d{2,4}[-/\. ]\d{1,2}[-/\. ]\d{1,2} 格式 2018-06-26
        res = r'\d{2,4}[-/\. ]\d{1,2}[-/\. ]\d{1,2}'
        fds = ''
        if re.search(res, dts):
            fds = re.search(res, dts).group()
        return fds

    def paseURL(burl, purl):

        # 提取字符串方法参数数据
        def getDEFP(dti):
            # dti = '  hhjkjhjka9  (  "n ame", \'22 2\'  )  '
            dti = str(dti).replace("\n", r"\n")
            ret = []
            for dst in dti[dti.find("(") + 1:dti.find(")")].split(','):
                oks = dst.strip().strip('"').strip('\'')
                ret.append(oks)
            return ret

        URL_TO = burl
        URL_BASE = URL_TO[0:URL_TO[8:].find('/') + 8]
        URL_BASE_THIS = URL_TO[0:URL_TO.rfind('/') + 1]

        url = str(purl)
        if url.find('(') > -1 and url[0:url.find('(')].find('/') == -1:
            url = getDEFP(url)[0]

        if url.startswith('http'):
            pass
        elif url.startswith('/'):
            url = URL_BASE + url
        else:
            url = URL_BASE_THIS + url

        return url

    poo = []

    def test_run(self, url, pw, pn, pt, pg, pr, pos):
        dbo = [pw, pn, pr]
        retss = self.processRequest(url, dbo)  # 执行
        self.printT('processRequest(url, dbo) ed')  # 打印
        # for r in retss:
        # printT(str(r))  # 打印
        self.printT('总数据数：' + str(len(retss)))  # 打印
        self.printT(url + '_end')  # 打印结束

    def printT(self, ps):
        spiders_data.sdata.test_list_page_prints.append(ps)
        print(">>>>>>>>>>>" + str(ps))


