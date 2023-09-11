import hashlib
from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.conf import settings


def index(request):
    try:
        username = request.session['username']
    except KeyError:
        username = None
    return render(request, "index.html", context={
        "username": username
    })


def login(request):
    method = request.method
    if method == "GET":
        return render(request, "login.html")
    elif method == "POST":
        username = request.POST.get("username")
        password = str(request.POST.get("pwd"))

        try:
            user = User.objects.get(username=username)
            res = password + settings.SECRET_KEY
            password = hashlib.md5(res.encode("utf-8")).hexdigest()
            if password == user.pwd:
                html = "<div><h1>恭喜！登录成功！</h1><div><a href='/index'>进入首页</a></div></div>"
                # 将用户信息存储到session里面
                # request.session['username'] = user.username

            else:
                html = "<div><h1>sorry,密码错误，请重新输入密码</h1><div><a href='/login'>重新登录</a></div></div>"


            return HttpResponse(html)

        except user.models.User.DoesNotExist:
            html = "<div><h1>sorry,用户名不存在</h1><div><a href='/login'>重新登录</a></div></div>"
            return HttpResponse(html)




def register(request):
    method = request.method # 请求方法
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
        password = str(request.POST.get("pwd"))

        res = password + settings.SECRET_KEY
        password = hashlib.md5(res.encode("utf-8")).hexdigest()

        email = request.POST.get("email")

        """添加数据"""
        User.objects.create(username=username, pwd=password, email=email, phone_number=phone_number)

        html = "<div><h1>恭喜，注册成功！</h1><div><a href='/login'>前往登录</div></div>"
        return HttpResponse(html)
