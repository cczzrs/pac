from django.test import TestCase
import json, pickle

# Create your tests here.

print('/pac/r/s/LP/test_list_page_printsi'.lstrip('/pac/r/s/'))
print('/pac/r/s/LP/test_list_page_printsi'.lstrip('/pac/r/s/').strip('/'))
print('/pac/r/s/LP/test_list_page_printsi'.lstrip('/pac/r/s/').strip('/').split('/'))
a = '/pac/r/s//LP/test_list_page_printsi'

print(a[a.find('//'):])
print(a[a.find('//'):].strip('/'))
print(a[a.find('//'):].strip('/').split('/'))
a = {'a'}
print('a' if a else '-')
