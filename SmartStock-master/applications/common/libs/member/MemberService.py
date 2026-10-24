import hashlib
import json
import random
import requests
import string

from applications.config import BaseConfig


class MemberService:

    @staticmethod
    def geneAuthCode(member_info=None):
        m = hashlib.md5()
        str = "%s-%s-%s" % (member_info.id, member_info.salt, member_info.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return ("".join(keylist))

    @staticmethod
    def getWeChatOpenid(code):
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={' \
              '2}&grant_type=authorization_code' \
            .format(BaseConfig.MIN_APP['appid'], BaseConfig.MIN_APP['appkey'], code)
        re = requests.get(url)
        res = json.loads(re.text)
        openid = None
        if "openid" in res:
            openid = res['openid']
        return openid

    @staticmethod
    def getWeChatAccessToken():
        url = 'https://api.weixin.qq.com/cgi-bin/token?appid={0}&secret={1}&grant_type=client_credential' \
            .format(BaseConfig.MIN_APP['appid'], BaseConfig.MIN_APP['appkey'])
        re = requests.get(url)
        res = json.loads(re.text)
        access_token = None
        if "access_token" in res:
            access_token = res['access_token']
        return access_token

    @staticmethod
    def getWeChatPhoneNumber(code):
        access_url = 'https://api.weixin.qq.com/cgi-bin/token?appid={0}&secret={1}&grant_type=client_credential' \
            .format(BaseConfig.MIN_APP['appid'], BaseConfig.MIN_APP['appkey'])
        re = requests.get(access_url)
        res = json.loads(re.text)
        access_token = None
        if "access_token" in res:
            access_token = res['access_token']

        phone_url = f'https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token={access_token}'

        headers = {"Content-Type": "application/json"}
        para = {'code': code}
        response = requests.post(phone_url, json=para, headers=headers)

        res = response.json()

        phone = None
        if res['errcode'] == 0:
            phone = res['phone_info']['phoneNumber']
            return {"phone": phone, "msg": "获取成功"}

        return {"phone": phone, "msg": res['errmsg']}

    @staticmethod
    def geneAuthCode2(member_info=None):
        m = hashlib.md5()
        str = "%s-%s-%s" % (member_info.id, member_info.username, member_info.enable)
        m.update(str.encode("utf-8"))
        return m.hexdigest()