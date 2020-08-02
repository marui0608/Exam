from django.contrib import admin
from django.urls import path, include, re_path

from account.views import RegisterView, ActiveUserView, ForCodeView, LoginView, index, ForgetPwdView, LogoutView, \
    ResetView, ModifyPwdView, weibo_login, Bindemail

urlpatterns = [
    # xadmin后台路由
    path('xadmin/', admin.site.urls),
    # 验证码
    path('captcha/', include('captcha.urls')),

    # 首页
    path("index/", index, name="index"),
    # 邮箱注册路由
    path('register/', RegisterView.as_view(), name='register'),
    # 邮件激活路由
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),
    # 手机号注册路由
    path('forcode/', ForCodeView.as_view(), name='forcode'),
    # 第三方登录
    path('social/', include('social_django.urls', namespace='social')),
    # 微博第三方登录路由
    path('weibo/', weibo_login, name="weibo"),
    # 微博登录后回调路由
    path("bindemail/", Bindemail.as_view(), name="Bindemail"),

    # 用户登陆路由
    path("login/", LoginView.as_view(), name="login"),
    # 用户注销路由
    path('logout/', LogoutView.as_view(), name="logout"),
    # 用户找回密码路由
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    # 用户重置密码路由
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),
    # 用户修改密码路由
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),

]
