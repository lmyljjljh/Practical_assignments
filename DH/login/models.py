from django.db import models


# Create your models here.
# 用户表
class User(models.Model):
    phone_number = models.CharField(max_length=255, unique=False)
    username = models.CharField(max_length=255, unique=False)
    password = models.CharField(max_length=255, unique=False)
    email = models.EmailField()
    state = models.BooleanField(default=True)

    class Meta:
        db_table = "user"


# 回答表（文字）
class answer_1(models.Model):
    question = models.CharField(max_length=255, unique=False)
    answer = models.CharField(max_length=255, unique=False)

    class Meta:
        db_table = "answer_1"


# 回答表（图片）
class answer_2(models.Model):
    question = models.ImageField(max_length=255, unique=False)
    answer = models.ImageField(max_length=255, unique=False)

    class Meta:
        db_table = "answer_2"

# 回答表（链接）
class answer_3(models.Model):
    question = models.CharField(max_length=255, unique=False)
    answer = models.CharField(max_length=255, unique=False)

    class Meta:
        db_table = "answer_3"


# 用户登录信息表
class login(models.Model):

    username = models.CharField(max_length=255, unique=False)
    ip = models.CharField(max_length=255, unique=False)
    # 浏览器名称
    browser = models.CharField(max_length=255, unique=False)
    # 时间
    time = models.DateTimeField(max_length=255, unique=False)

    class Meta:
        db_table = "login"


# 用户发送短语表
class phrase(models.Model):
    username = models.CharField(max_length=255, unique=False)
    # 短语
    ph = models.CharField(max_length=255, unique=False)
    # 时间
    time = models.DateTimeField(max_length=255, unique=False)

    class Meta:
        db_table = "phrase"


# 管理员
class AD(models.Model):
    username = models.CharField(max_length=255, unique=False)
    password = models.CharField(max_length=255, unique=False)

    class Meta:
        db_table = "AD"
