from django.test import TestCase
import time, threading
# Create your tests here.

tti = time.time()
tt = '===this page Count=%d, time_error=%d, find_cf=%d, find_error=%d, Exception=%d, BY_URL=%s,==='
tt = tt.split(',')
for sl in tt:
    if sl.find('Count') > -1:
        Count = sl[sl.rfind('=')+1:]
        print(Count)
    elif sl.find('time_error') > -1:
        Count = sl[sl.rfind('=')+1:]
        print(Count)
    elif sl.find('find_cf') > -1:
        Count = sl[sl.rfind('=')+1:]
        print(Count)
    elif sl.find('find_error') > -1:
        Count = sl[sl.rfind('=')+1:]
        print(Count)
    elif sl.find('Exception') > -1:
        Count = sl[sl.rfind('=')+1:]
        print(Count)
    elif sl.find('BY_URL') > -1:
        Count = sl[sl.rfind('=')+1:]
        print(Count)


t = [0,0,0,0,1]
print(t)
t.append(0)
t.append(0)
print(t)
t.append(0)
t = 'kk'
t2 = t
t3 = 'kk'
print(t)
print(hash(t))
print(hash(t2))
print(hash(t3))