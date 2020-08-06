import xadmin
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt

from account.views import RegisterView, ActiveUserView, ForCodeView, LoginView, ForgetPwdView, LogoutView, \
    ResetView, ModifyPwdView, weibo_login, Bindemail
from apps.competition.views import *

urlpatterns = [
    # xadmin后台路由
    path('xadmin/', xadmin.site.urls),
    # 验证码
    path('captcha/', include('captcha.urls')),

    # 首页
    path('', index, name='index'),
    # 邮箱注册路由
    path('register/', RegisterView.as_view(), name='register'),
    # 邮件激活路由
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),
    # 手机号注册路由
    path('forcode/', csrf_exempt(ForCodeView.as_view()), name='forcode'),
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

    # 首页信息
    path('detail/<str>', class_detail, name='detail'),
    #
    path('set/', include('competition.urls', namespace='set')),
    #
    path('rank/', rank, name='rank'),

]
