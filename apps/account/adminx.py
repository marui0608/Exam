import xadmin
from xadmin import views
from .models import *

class BaseSettings(object):
    # xadmin基础配置
    enable_themes = True   #开启主题功能
    use_bootswatch = True


class GlobalSettings(object):
    # 设置网站标题和页脚、收起菜单栏
    site_title = '考试系统后台管理页面'
    site_footer = 'EXAM - Powered By A-team-Group'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


xadmin.site.register(views.BaseAdminView,BaseSettings)
xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)





