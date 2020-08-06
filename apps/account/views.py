import datetime
import json
import random
import re

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View

from Exam.settings import APIKEY
from apps.account.models import UserProfile, EmailVerifyRecord, VerifyCode
from utils import weibo
from utils.email_send import send_register_eamil
from utils.yunpian import YunPian
from .forms import RegisterForm, LoginForm, ForgetPwdForm, ModifyPwdForm


# 激活用户功能视图
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功跳转到登录页面
                return render(request, "login.html", )
            # 验证码不对的时候跳转到激活失败页面
            else:
                return render(request, 'active_fail.html')
        else:
            return render(request, "register.html", {"msg": "您的激活链接无效"})


# 邮箱注册视图
class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():

            nick_name = request.POST.get('nick_name', None)
            user_name = request.POST.get('email', None)
            pass_word = request.POST.get('password', None)
            # 实例化一个user_profile对象
            user_profile = UserProfile()
            user_profile.nick_name = nick_name
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 对保存到数据库的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_eamil(user_name, 'register')
            return render(request, 'send_success.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


# 手机号注册视图
class ForCodeView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        mobile = request.POST.get('mobile', None)
        password = request.POST.get('password', None)
        if mobile:
            # 验证是否为有效手机号
            mobile_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
            res = re.search(mobile_pat, mobile)
            if res:
                if password:
                    # 生成手机验证码
                    c = random.randint(100000, 999999)
                    code = VerifyCode.objects.create(code=str(c), mobile=mobile)
                    code.save()
                    code = VerifyCode.objects.filter(code=str(c)).first()
                    yunpian = YunPian(APIKEY)
                    sms_status = yunpian.send_sms(code=code, mobile=mobile)
                    reg = UserProfile.objects.create(username=mobile, mobile=mobile, password=(make_password(password)))
                    reg.save()
                    msg = '发送成功，请查收!'
                    return HttpResponse(msg)
                else:
                    msg = '请输入账户密码!'
                    return HttpResponse(msg)
            else:
                msg = '请输入有效手机号码!'
                return HttpResponse(msg)
        else:
            msg = '手机号不能为空！'
            return HttpResponse(msg)


# 实现多用户类型登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Q查询集获取数据，实现手机号/邮箱/username都可以登录
            user = UserProfile.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            # 符合条件，加密密码，不可以明文存入
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用户登录视图
class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):

        login_form = LoginForm(request.POST)

        if login_form.is_valid():

            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)

            user = authenticate(username=user_name, password=pass_word)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})

            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})


        else:
            return render(request, 'login.html', {'login_form': login_form})


# 注销功能视图
class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


# 找回密码视图
class ForgetPwdView(View):

    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', None)
            # 发送邮箱
            send_register_eamil(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# 邮箱修改密码视图
class ModifyPwdView(View):

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致！"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


# 重置密码视图
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


# 跳转微博登录请求视图
def weibo_login(request):
    url = 'https://api.weibo.com/oauth2/' \
          'authorize?client_id=' + weibo.client_id + '&response_type=code&redirect_uri=' + weibo.redirect_uri
    return redirect(url)


# 微博登录后回调函数视图
class Bindemail(View):
    def get(self, request):
        code = request.GET.get('code')
        token = requests.post('https://api.weibo.com/oauth2/access_token?client_id=' + weibo.client_id + '&client_s'
                                                                                                         'ecret=' + weibo.client_secret + '&grant_type=authorization_'
                                                                                                                                          'code&redirect_uri=' + weibo.redirect_uri + '&code=' + code)
        text = json.loads(token.text)
        if token.status_code != 200:
            return redirect('/login/')
        access_token = text['access_token']
        uid = text['uid']
        url = 'https://api.weibo.com/2/users/show.json?access_token=' + access_token + '&uid=' + uid
        info2 = requests.get(url)
        info = info2.text
        info1 = json.loads(info)
        uid = info1['id']
        print(uid)
        name = info1['name']
        user = UserProfile.objects.filter(username=name).first()
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
        a = UserProfile.objects.create(username=str(name), last_login=datetime.datetime.now(), is_active=True,
                                       password=make_password(uid))
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        a.save()
        return redirect('/')
