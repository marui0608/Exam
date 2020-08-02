from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    gender_choices = (
        ('male', '男'),
        ('female', '女')
    )

    nick_name = models.CharField('昵称', max_length=50, default='')
    gender = models.CharField('性别', max_length=10, choices=gender_choices, default='female')
    adress = models.CharField('地址', max_length=100, default='')
    mobile = models.CharField("电话", max_length=11, null=True, blank=True)
    sfz = models.CharField('身份证', max_length=18, null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y%m', default='image/default.png', max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    send_choices = (
        ('register', '注册'),
        ('forget', '找回密码')
    )

    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField(choices=send_choices, max_length=10)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name


class VerifyCode(models.Model):
    """
    验证码
    """
    code = models.CharField("验证码", max_length=10, null=True)
    mobile = models.CharField("电话", max_length=11, null=True)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "短信验证"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
