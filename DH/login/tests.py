from random import randint

from django.test import TestCase

# Create your tests here.
# 生成验证码
from login.fasong import sms

params = "{'code':%d}" % (randint(1000, 100000))
# para = request.GET.get('phone_numbers')
res = sms.send('17771569161', params)