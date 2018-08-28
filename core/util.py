import re
import time
import xlwt
import xlrd
from dateutil import parser


# 提取日志中参数值
def get_log_key_value(pstr, key):
    for sl in pstr.split(','):
        if sl.find(key) > -1:
            return sl[sl.rfind(key+'=') + len(key) + 1:]


# 提取参数规则 key
def get_resolve_key(request):
    return request.session.get('resolve_key')


# 数组（array）提取其中对象属性（k）值的数组，是否值唯一（qy）默认唯一
def find_p1(array, k, qy=True):
    ret = {}
    if qy:
        for i in array:
            if type(i) == type({}) and k in i.keys():
                ret.update({i[k]: 'true'})
            elif hasattr(i, k):
                ret.update({getattr(i, k): 'true'})
        ret = list(ret.keys())
    else:
        ret = []
        for i in array:
            if type(i) == type({}) and k in i.keys():
                ret.append(i[k])
            elif hasattr(i, k):
                ret.append(getattr(i, k))

    return ret


# 数组提取其中对象属性值等于 zi 的对象
def find_p(array, **p):
    ret = []
    ro = {}
    for i in array:
        ro = i
        for k in p.keys():
            if hasattr(i, k) and getattr(i, k) == p[k]:
                pass
            else:
                ro = {}
                break
        if ro:
            ret.append(ro)
    return ret


# 提取时间格式数据
def getDT(dti=1):
    return time.strftime("%Y-%m-%d" if dti == 1 else "%Y-%m-%d %H:%M:%S", time.localtime())


def FPDate(dts, rtype='string'):
    dts = str(dts).replace("\n", r"\n")
    # \d{2,4}[-/\. ]\d{1,2}[-/\. ]\d{1,2} 格式 2018-06-26
    res = r'\d{2,4}[-/\. ]\d{1,2}[-/\. ]\d{1,2}'
    # \d{1,2}[-/\. ]\d{1,2} 格式 06-26
    res2 = r'\d{1,2}[-/\. ]\d{1,2}'
    # \d{2,4}年\d{1,2}月\d{1,2}日 格式 2018年06月26日
    res3 = r'\d{2,4}年\d{1,2}月\d{1,2}日'
    fds = ''
    no_year = False
    if re.search(res, dts):
        fds = re.search(res, dts).group()
    elif re.search(res2, dts):
        fds = re.search(res2, dts).group()
        no_year = True
    elif re.search(res3, dts):
        fds = re.search(res3, dts).group().replace('年', '-').replace('月', '-').replace('日', '')

    if rtype == 'date':
        fds = parser.parse(fds)
        if no_year and (fds - parser.parse(getDT())).days > 0:
            fds = fds.replace(year=fds.year-1)
    return fds


def paseURL(url_b, url_p):
    # 提取字符串方法参数数据
    def getDEFP(dti):
        # dti = '  hhjkjhjka9  (  "n ame", \'22 2\'  )  '
        dti = str(dti).replace("\n", r"\n")
        ret = []
        for dst in dti[dti.find("(") + 1:dti.find(")")].split(','):
            oks = dst.strip().strip('"').strip('\'')
            ret.append(oks)
        return ret

    URL_TO = url_b
    URL_BASE = URL_TO[0:URL_TO[8:].find('/') + 8]
    URL_BASE_THIS = URL_TO[0:URL_TO.rfind('/') + 1]

    url = str(url_p)
    if url.find('(') > -1 and url[0:url.find('(')].find('/') == -1:
        url = getDEFP(url)[0]

    if url.startswith('http'):
        pass
    elif url.startswith('/'):
        url = URL_BASE + url
    else:
        url = URL_BASE_THIS + url

    return url


def biuderEXECL(dboss, down_url):
    # 创建一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    '''
        Workbook类初始化时有encoding和style_compression参数
        encoding:设置字符编码，一般要这样设置：w = Workbook(encoding='utf-8')，就可以在excel中输出中文了。
        默认是ascii。当然要记得在文件头部添加：
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-
        style_compression:表示是否压缩，不常用。
    '''
    # 创建一个sheet对象，一个sheet对象对应Excel文件中的一张表格。
    # 在电脑桌面右键新建一个Excel文件，其中就包含sheet1，sheet2，sheet3三张表
    sheet = book.add_sheet('pac', cell_overwrite_ok=True)
    # 其中的test是这张表的名字,cell_overwrite_ok，表示是否可以覆盖单元格，其实是Worksheet实例化的一个参数，默认值是False
    # 向表test中添加数据

    row = 0
    for dbos in dboss:
        cel = 0
        for dbo in dbos:
            sheet.write(row, cel, dbo)
            cel += 1
        row += 1

    # 最后，将以上操作保存到指定的Excel文件中
    # down_url = r'C:/Users/cong/Desktop/download/pac_excel/pac_excel' + getDT() + '_' + str(time.time())[-3:] + '.xls'
    book.save(down_url)  # 在字符串前加r，声明为raw字符串，这样就不会处理其中的转义了。否则，可能会报错
    return down_url


def read_xls(xlsfile):
    rets = []
    # xlsfile = r"C:\Users\Administrator\Desktop\test\Account.xls"# 打开指定路径中的xls文件
    book = xlrd.open_workbook(xlsfile)  # 得到Excel文件的book对象，实例化对象
    sheet0 = book.sheet_by_index(0)  # 通过sheet索引获得sheet对象
    sheet_name = book.sheet_names()[0]  # 获得指定索引的sheet表名字
    sheet1 = book.sheet_by_name(sheet_name)  # 通过sheet名字来获取，当然如果知道sheet名字就可以直接指定
    nrows = sheet0.nrows  # 获取行总数
    # 循环打印每一行的内容
    for i in range(nrows):
        print(sheet1.row_values(i))
        rets.append(sheet1.row_values(i))
    ncols = sheet0.ncols    # 获取列总数
    print(ncols)
    row_data = sheet0.row_values(0)     # 获得第1行的数据列表
    col_data = sheet0.col_values(0)     # 获得第1列的数据列表
    print(row_data)
    print(col_data)
    # 通过坐标读取表格中的数据
    cell_value1 = sheet0.cell_value(0, 0)
    cell_value2 = sheet0.cell_value(0, 1)
    print(cell_value1)
    print(cell_value2)

    return rets

