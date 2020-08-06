from captcha.fields import CaptchaField
from django import forms


class RegisterForm(forms.Form):
    '''
    注册验证表单
    '''
    nick_name = forms.CharField(required=True, min_length=1)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # 验证码
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetPwdForm(forms.Form):
    '''忘记密码'''
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class LoginForm(forms.Form):
    """
    登陆验证码
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class ModifyPwdForm(forms.Form):
    '''重置密码'''
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
