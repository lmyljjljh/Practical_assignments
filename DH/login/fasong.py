from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

ACCESS_KEY_ID = "LTAI5tFMMBaVEtSg8T1oUBQz"  # 用户AccessKey
ACCESS_KEY_SECRET = "eUJCBn0NMjaZFaw1cqeSjlskwHmKRH"  # Access Key Secret


class SMS:
    def __init__(self, signName, templateCode):
        self.signName = signName
        self.templateCode = templateCode
        self.client = client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, 'cn-hangzhou')

    def send(self, phone_numbers, template_param):
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('PhoneNumbers', phone_numbers)
        request.add_query_param('SignName', self.signName)
        request.add_query_param('TemplateCode', self.templateCode)
        request.add_query_param('TemplateParam', template_param)
        response = self.client.do_action_with_exception(request)
        return response


# 发送短信的人
sms = SMS("lmyljjljh", "SMS_463660161")
