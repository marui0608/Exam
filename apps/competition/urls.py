from django.urls import path
from competition.views import *

app_name = 'set'

urlpatterns = [
    # 录入、配置题库首页
    path('set_index/',set_index,name='set_index'),
    # 录制题库
    path('set_bank/',set_bank,name='set_bank'),
    # 模板下载
    path('template_download/',template_download,name='template_download'),
    # 配置考试
    path('set_test/',set_test,name='set_test'),
    path('type/',type,name='type'),
    # 考试信息
    path('test_info/<id>',test_info,name='test_info'),
    # 开始考试
    path('test_start/<id>',test_start,name='test_start'),
]