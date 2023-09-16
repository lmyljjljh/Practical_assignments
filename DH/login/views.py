import datetime
import hashlib
import time
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, answer_1, AD, phrase
from django.conf import settings
from .models import login as DL
from login.fasong import sms
from random import randint
import re

# 首页视图
def index(request):
    # 首先获取页面传输的问题
    keywords = answer_1.objects.values_list('question', flat=True)
    # methods = request.POST.get('methods', '')
    # 判断请求是否为POST也就是表单传过来的
    if request.method == 'POST':
        # 获取表单传过来的问题
        question = request.POST.get('question', '')
        response = None
        if question:
            try:
                # 在数据库中查找相应的问题
                response = answer_1.objects.get(question=question)
                # 将此时用户行为记录
                phrase.objects.create(username=request.session['username'], ph=question,
                                      time=timezone.now())
            except answer_1.DoesNotExist:
                response = None

        return render(request, 'index.html',
                      {'question': question, 'response': response, 'keywords': keywords, 'key': "0"})
    # 页面首次进入
    elif request.method == 'GET':
        welcome_message = "欢迎来到 Chat Room"
        # print("*********************************")
        # print(type(request.method))
        return render(request, 'index.html',
                      {'keywords': keywords, 'welcome_message': welcome_message, 'methods': request.method})
    else:
        return render(request, 'index.html', {'keywords': keywords})


# 用户管理视图
def yonghuguanli(request):
    # username = User.objects.values('username')
    # password = User.objects.values('password')
    # email = User.objects.values('email')
    # phone_number = User.objects.values('phone_number')
    # username = [entry['username'] for entry in username]
    # password = [entry['password'] for entry in password]
    # email = [entry['email'] for entry in email]
    # phone_number = [entry['phone_number'] for entry in phone_number]
    user = User.objects.all()
    # print(User.objects.values('id'))
    # 2、组织数据
    context = {
        'yhs': user
    }
    return render(request, 'yonghuguanli.html', context=context)


# 管理员首页视图
def ad(request):
    return render(request, 'ad.html')


# 回答文字管理视图
def huidawenzi(request):
    answer = answer_1.objects.all()
    context = {
        'answers': answer
    }
    return render(request, 'wdwz.html', context=context)


# 管理员添加用户视图
def add(request):
    method = request.method
    if method == "POST":
        username = request.POST.get("addName")
        password = str(request.POST.get("addCode"))
        email = request.POST.get('addEmail')
        phone_number = request.POST.get('addNumber')
        # print("*******************************************")
        """密码加密"""
        res = password + settings.SECRET_KEY
        password = hashlib.md5(res.encode("utf-8")).hexdigest()
        # print("*******************************************")
        # print(username)
        # print(password)
        # print(email)
        # print(phone_number)
        """添加数据"""
        User.objects.create(username=username, password=password, email=email, phone_number=phone_number)

        return redirect('/yh/')


# 管理员添加问题回答视图
def addhdwz(request):
    method = request.method
    if method == "POST":
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        """添加数据"""
        answer_1.objects.create(question=question, answer=answer)
        return redirect('/hdwz/')


# 管理员删除某个问题视图
def delhdwz(request):
    try:
        response_id = request.GET.get('id')
        # print('********************************')
        # print(response_id)
        response = answer_1.objects.get(id=response_id)
        response.delete()
        return redirect('/hdwz/')  # 重定向到展示所有数据库项的页面
    except User.DoesNotExist:
        return redirect('/hdwz/')  # 处理不存在的情况，重定向到展示所有数据库项的页面


# 管理员删除用户视图
def drop(request):
    try:
        response_id = request.GET.get('id')
        # print('********************************')
        # print(response_id)
        response = User.objects.get(id=response_id)
        response.delete()
        return redirect('/yh/')  # 重定向到展示所有数据库项的页面
    except User.DoesNotExist:
        return redirect('/yh/')  # 处理不存在的情况，重定向到展示所有数据库项的页面


# 管理员重置用户密码视图
def cz(request):
    try:
        response_id = request.GET.get('id')
        # print('********************************')
        # print(response_id)
        user = User.objects.get(id=response_id)
        password = '123456'
        res = password + settings.SECRET_KEY
        password = hashlib.md5(res.encode("utf-8")).hexdigest()
        """修改数据"""
        user.password = password
        user.save()
        return redirect('/yh/')  # 重定向到展示所有数据库项的页面
    except User.DoesNotExist:
        return redirect('/yh/')  # 处理不存在的情况，重定向到展示所有数据库项的页面


# 管理员禁止用户登录视图
def jz(request):
    try:
        response_id = request.GET.get('id')
        # print('********************************')
        # print(response_id)
        user = User.objects.get(id=response_id)
        """修改数据"""
        user.state = False
        user.save()
        return redirect('/yh/')  # 重定向到展示所有数据库项的页面
    except User.DoesNotExist:
        return redirect('/yh/')  # 处理不存在的情况，重定向到展示所有数据库项的页面


# 管理员解除禁止用户登录视图
def jcjz(request):
    try:
        response_id = request.GET.get('id')
        # print('********************************')
        # print(response_id)
        user = User.objects.get(id=response_id)
        """修改数据"""
        user.state = True
        user.save()
        return redirect('/yh/')  # 重定向到展示所有数据库项的页面
    except User.DoesNotExist:
        return redirect('/yh/')  # 处理不存在的情况，重定向到展示所有数据库项的页面


# 管理员登录视图
def adlogin(request):
    method = request.method
    if method == "GET":
        return render(request, "ADlogin.html")
    elif method == "POST":
        username = request.POST.get("username")
        password = str(request.POST.get("password"))
        try:
            ad = AD.objects.get(username=username)
            if password == ad.password and ad is not None:
                return redirect('/ad/')
        except AD.DoesNotExist:
            html = "<div><h1>sorry,用户名不存在</h1><div><a href='/login'>重新登录</a></div></div>"
            return HttpResponse(html)


# 用户登录视图
def login(request):
    method = request.method
    if method == "GET":
        return render(request, "login.html")
    elif method == "POST":
        username = request.POST.get("username")
        password = str(request.POST.get("password"))

        try:
            user = User.objects.get(username=username)
            res = password + settings.SECRET_KEY
            password = hashlib.md5(res.encode("utf-8")).hexdigest()
            state = user.state
            if password == user.password and state == True:
                # 将用户信息存储到session里面
                request.session['username'] = user.username
                # # 获取访问者IP
                ip = request.META.get("REMOTE_ADDR")
                user_agent = request.META.get('HTTP_USER_AGENT', '')
                # 在用户代理字符串中查找浏览器类型
                if 'MSIE' in user_agent:
                    browser = 'Internet Explorer'
                elif 'Firefox' in user_agent:
                    browser = 'Firefox'
                elif 'Chrome' in user_agent:
                    browser = 'Google Chrome'
                elif 'Safari' in user_agent and 'Chrome' not in user_agent:
                    browser = 'Safari'
                else:
                    browser = 'Unknown'
                # print("**********************************")
                times = timezone.now()
                # print(times)
                DL.objects.create(username=username, ip=ip, time=times, browser=browser)
                return redirect('/index/')
            else:
                html = "<div><h1>sorry,用户名不存在或密码错误，请重新输入</h1><div><a href='/login'>重新登录</a></div></div>"
                return HttpResponse(html)
        except User.DoesNotExist:
            html = "<div><h1>sorry,用户名不存在</h1><div><a href='/login'>重新登录</a></div></div>"
            return HttpResponse(html)


# 管理员修改问题回答视图1
def huidaxg(request):
    method = request.method
    if method == "GET":
        return render(request, "wdwz.html")
    elif method == "POST":
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        id = request.POST.get("id")
        ans = answer_1.objects.get(id=id)
        """修改数据"""
        ans.answer = answer
        ans.question = question
        ans.save()
        return redirect('/hdwz/')


# def chat_room(request):
#     keywords = answer_1.objects.values_list('question', flat=True)
#
#     if request.method == 'POST':
#         question = request.POST.get('question', '')
#         response = None
#         if question:
#             try:
#                 response = answer_1.objects.get(question=question)
#             except answer_1.DoesNotExist:
#                 response = None
#
#         return render(request, 'index.html',
#                       {'question': question, 'response': response, 'keywords': keywords, 'key': 0})
#     elif request.method == 'GET':
#         print("*********************************")
#         return render(request, 'index.html', {'keywords': keywords, 'key': 1})
#
#     else:
#         return render(request, 'index.html', {'keywords': keywords})

# 管理员修改问题回答视图2
def huidaxg1(request):
    try:
        response_id = request.GET.get('id')
        # print('********************************')
        # print(response_id)
        response = answer_1.objects.get(id=response_id)

        # 2、组织数据
        context = {
            'response': response
        }
        return render(request, 'huidaxg.html', context=context)
    except answer_1.DoesNotExist:
        return redirect('/yh/')  # 处理不存在的情况，重定向到展示所有数据库项的页面


# 用户注册视图
def register(request):
    method = request.method  # 请求方法
    if method == "GET":
        return render(request, "register.html")
    elif method == "POST":
        username = request.POST.get("username")
        phone_number = request.POST.get('phone_number')
        res = User.objects.filter(username=username)

        """验证用户名是否存在"""
        if res:
            html = "<div><h1>sorry,用户名已被注册，请尝试新的用户名</h1><div><a href='/register'>重新注册</a></div></div>"
            return HttpResponse(html)

        """密码加密"""
        password = str(request.POST.get("password"))

        res = password + settings.SECRET_KEY
        password = hashlib.md5(res.encode("utf-8")).hexdigest()

        email = request.POST.get("email")

        """添加数据"""
        User.objects.create(username=username, password=password, email=email, phone_number=phone_number)

        # html = "<div><h1>恭喜，注册成功！</h1><div><a href='/login'>前往登录</div></div>"
        return redirect('/login/')
        # return HttpResponse(html)


# 找回密码视图
def zh(request):
    method = request.method  # 请求方法
    if method == "GET":
        return render(request, "zhaohui.html")
    elif method == "POST":
        username = request.POST.get("username")
        """密码加密"""
        password = str(request.POST.get("password"))

        res = password + settings.SECRET_KEY
        password = hashlib.md5(res.encode("utf-8")).hexdigest()

        email = request.POST.get("email")

        """修改数据"""
        user = User.objects.get(username=username)
        user.password = password
        user.save()
        # User.objects.create(username=username, password=password, email=email, phone_number=phone_number)

        # html = "<div><h1>恭喜，注册成功！</h1><div><a href='/login'>前往登录</div></div>"
        return redirect('/login/')


# 管理员统计登录信息视图
def tj1(request):
    dls = DL.objects.all()
    context = {
        'dls': dls
    }
    return render(request, 'tj1.html', context=context)


# 管理员统计用户发送信息视图
def tj2(request):
    phrs = phrase.objects.all()
    context = {
        'phrs': phrs
    }
    return render(request, 'tj2.html', context=context)

# 获取手机验证码
def Aliyun_register(request):
    method = request.method  # 请求方法
    if method == "GET":
        context = {
            'params': None,
            'phone': None
        }
        print("*******************************************************")
        return render(request, 'shoujilogin.html', context=context)
    elif method == "POST":
        # 生成验证码
        params = "{'code':%d}" % (randint(1000, 100000))
        para = request.POST.get('phone')
        print(para)

        res = sms.send(para, params)
        context = {
            'params': params,
            'phone': para
        }
        return render(request, 'shoujilogin.html', context=context)
    # return HttpResponse(res)

# 手机号登录页面视图
def shjlogin(request):
    context = {
        'params': None,
        'phone': None
    }
    # print("*******************************************************")
    return render(request, 'shoujilogin.html', context=context)

# 报错返回视图
def errof(request):
    # 在这里使用 my_parameter
    param1 = request.GET.get('param1')
    param2 = request.GET.get('param2')
    context = {
        'params': param1,
        'phone': param2
    }
    return render(request, 'shoujilogin.html', context=context)


# 手机号登录视图
def sjlogin(request):
    method = request.method  # 请求方法
    if method == "GET":
        return render(request, "zhaohui.html")
    elif method == "POST":
        phone = request.POST.get("phone")
        param = request.POST.get("param")
        yzm = request.POST.get("yzm")
        res = User.objects.filter(phone_number=phone)
        print(res)

        """验证手机号是否存在"""
        if res:
            """验证验证码是否正确"""
            # print(111111111111111111111111111)
            yzm = re.findall(r'\d+', yzm)
            # print(yzm[0])
            # print(param)
            if param == yzm[0]:
                user = User.objects.get(phone_number=phone)
                # 将用户信息存储到session里面
                # print(111111111111111111111111111)
                request.session['username'] = user.username
                # # 获取访问者IP
                ip = request.META.get("REMOTE_ADDR")
                user_agent = request.META.get('HTTP_USER_AGENT', '')
                # 在用户代理字符串中查找浏览器类型
                if 'MSIE' in user_agent:
                    browser = 'Internet Explorer'
                elif 'Firefox' in user_agent:
                    browser = 'Firefox'
                elif 'Chrome' in user_agent:
                    browser = 'Google Chrome'
                elif 'Safari' in user_agent and 'Chrome' not in user_agent:
                    browser = 'Safari'
                else:
                    browser = 'Unknown'
                # print("**********************************")
                times = timezone.now()
                # print(times)
                DL.objects.create(username=user.username, ip=ip, time=times, browser=browser)
                return redirect('/index/')
            else:
                print(222222222222222222222222222222222)
                context = {
                    'params': param,
                    'phone': phone
                }
                # return redirect('/index/')
                return render(request, "erro.html", context=context)

        else:
            html = "<div><h1>sorry,用户未被注册，请尝试创建用户</h1><div><a href='/register'>前往注册</a></div></div>"
            return HttpResponse(html)
