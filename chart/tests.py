
from core import util, settings as set
from selenium.webdriver import Chrome

tt= {'vv': 'xx'}

rs = range(32)
c = Chrome(executable_path=set.EXECUTABLE_PATH)
for r in rs:
    url = 'http://xiaobai.ruanjiandown.com:7457/iso/732_xb_17_6_%d.iso' % r
    c.get(url)
    if c.title.startswith('404'):
        continue
    else:
        print(url)


