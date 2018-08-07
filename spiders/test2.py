# coding=utf-8
import re
import time
from lxml import etree
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def processRequest(URL_TO, dbo):
    print("##########FMiddleware process_request##########")

    contentPage = 1
    contentCount = 0
    DB_URLS = []
    THIS_URLS = {}

    options = Options()
    # options.add_argument('-headless')  # 无头参数
    driver = Firefox(executable_path='geckodriver', firefox_options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
    wait = WebDriverWait(driver, timeout=10)

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
    dbo_wait = dbo[0]  # {"wait": '//div[@class="right_left"]'}
    dbo_next = dbo[1]  # {"next": '//div[@id="page_div"]//a[contains(text(), "下一页")]'}
    dbo_sources = dbo[2]  # {"trs": [['//div[@class="right_left"]//table[2]//tr']]}
    dbo_source = dbo[3]  # {"tr": {"news_title": [['//td[@height="22"]//a/text()']],
    #                              "url_source": [['//td[@height="22"]//a/@href']],
    #                              "news_date": [['//td[@align="center"]//a/text()']]}}

    driver.get(URL_TO)  # 加载
    # driver.set_script_timeout(15)

    wait.until(EC.visibility_of_element_located((By.XPATH, dbo_wait["wait"])))  # 等待渲染数据
    print('driver.page_source=' + driver.page_source.replace('\n', ''))

    while True:
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
            break
        print('lbs=' + str(lbs))

        find_error = 0  # 重复或丢弃的数据数
        error_t = 0
        find_cf = 0
        dbo_st = dbo_source['tr']
        for ld in lbs:
            contentCount += 1
            print('###########' + str(contentCount) + '###########' + ld)
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
                        if ld_ed[0] == '#':
                            ti = str(tr_is[len(tr_is)-1])
                            ld_ed = lb_f_ef.xpath(ti[:ti.rfind('@')] + "@onclick")
                        ldo[dtk] += ld_ed
                    if len(ldo[dtk]) > 0:
                        ldo[dtk] = ''.join(ldo[dtk])
                    else:
                        ldo[dtk] = ''
            except IOError as e:
                error_t += 1
                print('BaseException error_t=' + str(error_t) + ' by ' + dtk + ' \te:' + str(e))
                continue

            if not ldo['news_title'] or not ldo['url_source']:  # 剔除垃圾数据
                find_error += 1
                print('find_error=' + str(find_error))
                continue

            ldo['news_date'] = FPDate(ldo['news_date'])
            ldo['url_source'] = paseURL(URL_TO, ldo['url_source'])
            if (ldo['url_source'] in DB_URLS) or (ldo['url_source'] in THIS_URLS.keys()):  # 判断是否已有该 url 数据
                find_cf += 1
                print('find_cf=' + str(find_cf))
            else:
                THIS_URLS[ldo['url_source']] = ldo

            print('ldo=' + str(ldo))

        print('===this page Count=%d, find_cf=%d, find_error=%d, Exception=%d===' % (len(lbs), error_t, find_error, find_cf))
        if len(lbs) == error_t + find_error + find_cf:
            print('!!!!!!!!!!find all data over!!!!!!!!!!')
            break

        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, dbo_next['next']))).click()  # 等待渲染后点击下一页，没有下一页等待超时退出
            contentPage += 1
            print('###########next' + str(contentPage) + '##########')

            time.sleep(1.200)  # 等待 1.2 秒

            wait.until(EC.visibility_of_element_located((By.XPATH, dbo_wait['wait'])))  # 等待渲染数据
            print('###########next data##########')

        except BaseException as e:
            print('###########data over########## e=' + str(e))
            break

    print('contentPage=' + str(contentPage))
    print('contentCount=' + str(contentCount))
    driver.quit()

    return THIS_URLS


def FPDate(dts):
    dts = str(dts).replace("\n", r"\n")
    # \d{2,4}[-/\. ]\d{1,2}[-/\. ]\d{1,2} 格式 2018-06-26
    res = r'\d{2,4}[-/\. ]\d{1,2}[-/\. ]\d{1,2}'
    # \d{1,2}[-/\. ]\d{1,2} 格式 06-26
    res2 = r'\d{1,2}[-/\. ]\d{1,2}'
    fds = ''
    if re.search(res, dts):
        fds = re.search(res, dts).group()
    elif re.search(res2, dts):
        fds = re.search(res2, dts).group()
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


if __name__ == '__main__':
    url = 'http://ghgtw.beijing.gov.cn/module/idea/que_discusslist.jsp?webid=1&appid=1&typeid=2&showtype=all'
    dbo = [
        {"wait": '//div[@class="right_left"]'},
        {"next": '//input[@value="GO"]'},
        {"trs": [['/html/body/div[3]/div/div/div[1]/div[2]/div/table[2]/tbody/tr/td/a/../..']]},
        {"tr": {"news_title": [['//td[@height="22"]//a/text()']],
                "url_source": [['//td[@height="22"]//a/@href']],
                "news_date": [['//td[@align="center"]//a/text()']]}
         }
    ]
    url = 'http://www.xygh.gov.cn/guihua/yongdi/'
    dbo = [
        {"wait": '//div[@class="listbox"]'},
        {"next": '//a[contains(text(), "下一页")]'},
        {"trs": [['/html/body/div[1]/div[4]/div[2]/ul/li']]},
        {"tr": {"news_title": [['//a/text()'], ['//a/strong/text()']], "url_source": [['//a//@href']],
                "news_date": [['//span/text()']]}}
    ]
    retss = processRequest(url, dbo)  # 执行
    print('processRequest(url, dbo) ed')  # 打印
    for r in retss:
        print(str(r))  # 打印
    print('总数据数' + str(len(retss)))  # 打印



