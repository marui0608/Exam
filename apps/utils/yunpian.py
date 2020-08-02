import requests


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        parmas = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【张润钰】您的验证码是{code}。如非本人操作，请忽略本短信。'.format(code=code)
        }
        r = requests.post(self.single_send_url, data=parmas)
        return r


if __name__ == '__main__':
    yun_pian = YunPian('4e9a8211181ab7ab112c73aae072820c')
    yun_pian.send_sms('2020', '15535533934')
