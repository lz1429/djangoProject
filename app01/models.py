"""
在终端Terminal中先后执行以下两条命令 创建数据库表：
    python manage.py makemigrations
    python manage.py migrate
# 在终端Terminal中执行以下任意一条命令 创建另一模块：
    python manage.py startapp app02
    或 django-admin startapp app02
"""
from django.db import models


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='部门名称', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, default=1)
    create_date = models.DateField(verbose_name="入职时间")
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE,
                               default=49)
    account = models.DecimalField(verbose_name="月薪", max_digits=10, decimal_places=2, default=8000)
    mobile = models.CharField(verbose_name="手机号码", max_length=11)
    birth_date = models.DateField(verbose_name="出生日期")


class Admin(models.Model):
    """ 管理员 """
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class City(models.Model):
    """ 城市 """
    name = models.CharField(verbose_name="名称", max_length=32)
    count = models.IntegerField(verbose_name="人口")
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to='city/')
