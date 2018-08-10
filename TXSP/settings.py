import platform


# 判断当前操作系统
this_os = 'Windows' in list(platform.uname())

# 运行模式 DEBUG
IS_DEBUG = True if this_os else False

# 是否打印详情日志
PRINT_LOG = True if this_os else False

# 默认循环下一页次数
TEST_RUN_COUNT = 3 if this_os else 1000

# 文件生成地址，供下载使用  (前面是Windows路径，后面是linux路径)
DOWN_URL = r'C:/Users/cong/Desktop/download/pac_excel/' if this_os else r'/opt/pac/download/pac_excel/'

# 爬虫爬取的图片及文件保存地址
WEB_DOWN_FILE_PATH = r'C:/Users/cong/Desktop/download' if this_os else r'/opt/pac/download'
# 爬虫爬取的图片及文件，如果已有是否重新下载，否则略过
WEB_DOWN_FILE_REDOWN = False

# 静态文件 static 集成路径
STATIC_ROOT = r'C:/Users/cong/Desktop/download/static/' if this_os else r'/opt/pac/download/static/'

# 谷歌浏览器插件路径 // 找得到？(环境变量)
EXECUTABLE_PATH = 'chromedriver'
# 浏览器头部信息（下载文件时需要携带）
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
# 运行是否显示浏览器
EXECUTABLE_RUN_SHOW = True if this_os else False
# 页面加载超时时间 s
WEBDRIVERWAIT_TIMEOUT = 10
# 使用的线程池数 -- 同时执行多少个任务
TESKS_THREAD_POOL_EXECUTOR_LEN = 3
# 使用的线程池数 -- 单个任务
TESK_THREAD_POOL_EXECUTOR_LEN = 5 if this_os else 10


# 数据库配置
DATABASES_ENGINE =  'django.db.backends.mysql'  # 数据库的类型
DATABASES_NAME =    'pactera'   if this_os else 'pac'              # 所使用的的数据库的名字
DATABASES_USER =    'root'      if this_os else 'root'             # 数据库服务器的用户
DATABASES_PASSWORD ='root'      if this_os else '1234567890'      # 密码
DATABASES_HOST =    '127.0.0.1'if this_os else '211.159.172.213'  # 主机
DATABASES_PORT =    '3306'      if this_os else '3309'               # 端口

