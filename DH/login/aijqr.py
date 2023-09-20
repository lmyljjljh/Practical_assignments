import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tbp.v20190627 import tbp_client, models


class TencentBot:
    def __init__(self, secret_id, secret_key):
        self.secret_id = secret_id
        self.secret_key = secret_key

    def chat(self, input_text):
        try:
            cred = credential.Credential(self.secret_id, self.secret_key)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tbp.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = tbp_client.TbpClient(cred, "", clientProfile)

            req = models.TextProcessRequest()
            params = {
                "BotId": "0be3c628-17bb-405a-897d-04cc61d8b781",
                "BotEnv": "dev",
                "TerminalId": "test1",
                "InputText": input_text
            }
            req.from_json_string(json.dumps(params))

            resp = client.TextProcess(req).to_json_string()
            resp = json.loads(resp)
            return resp['ResponseText']

        except TencentCloudSDKException as err:
            return str(err)


bot = TencentBot("", "")
