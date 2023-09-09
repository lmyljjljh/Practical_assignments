from django.db import models


# Create your models here.
# 用户表
class User(models.Model):
    phone_number = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=False, primary_key=True)
    password = models.CharField(max_length=255, unique=False)
    email = models.EmailField()

    class Meta:
        db_table = "user"


# 回答表（文字）
class answer_1(models.Model):
    question = models.CharField(max_length=255, unique=True)
    answer = models.CharField(max_length=255, unique=True)


# 回答表（图片）
class answer_2(models.Model):
    question = models.ImageField(max_length=255, unique=True)
    answer = models.ImageField(max_length=255, unique=True)


# 回答表（链接）
class answer_3(models.Model):
    question = models.CharField(max_length=255, unique=True)
    answer = models.CharField(max_length=255, unique=True)


# 用户登录信息表
class login(models.Model):
    username = models.CharField(max_length=255, unique=False, primary_key=True)
    ip = models.CharField(max_length=255, unique=True)
    # 浏览器名称
    browser = models.CharField(max_length=255, unique=True)
    # 时间
    time = models.TimeField(max_length=255, unique=True)

# 用户发送短语表
class phrase(models.Model):
    username = models.CharField(max_length=255, unique=False, primary_key=True)
    # 短语
    ph = models.CharField(max_length=255, unique=True)
    # 时间
    time = models.TimeField(max_length=255, unique=True)


# 管理员
class AD(models.Model):
    username = models.CharField(max_length=255, unique=False, primary_key=True)
    password = models.CharField(max_length=255, unique=False)
