import base64
import io
import json
from typing import Tuple, List, Any

import requests


# using MommyTalk API
# Latex OCR
class Matpix_OCR:
    headers = {
        'app_id': 'jimmychou_vip_qq_com_f65a7e',
        'app_key': '8b2a5b2fc757a6966d18',
        'Content-type': 'application/json'
    }

    @staticmethod
    def image_uri(filename: str or io.BytesIO):
        if type(filename) is str:
            image_data = open(filename, "rb").read()
        elif type(filename) is io.BytesIO:
            image_data = filename.getvalue()
            filename.close()
        return "data:image/png;base64," + base64.b64encode(image_data).decode()

    @staticmethod
    def mathpix_ocr(image_src: str, timeout=30) -> Tuple:
        service_url = 'https://api.mathpix.com/v3/latex'
        payload = {'src': image_src,
                   "ocr": ["math", "text"],
                   'formats': ['latex_simplified']}
        
        # 连接错误重试3次
        i = 0
        while i < 3:
            try:    
                response = requests.post(service_url, data=json.dumps(payload), headers=Matpix_OCR.headers,
                                 timeout=timeout)
                if response.status_code == 200:
                    break
            except Exception as e:
                i += 1

        result = json.loads(response.text)
        if 'error_info' not in result.keys():
            return 1, result['latex_simplified']
        else:
            return 0, None

    @staticmethod
    def ocr(img_bytes: io.BytesIO):
        image_src = Matpix_OCR.image_uri(img_bytes)
        return Matpix_OCR.mathpix_ocr(image_src, timeout=3)


# Baidu API
# My Account Common API
class BaiduOCR:
    def __init__(self):
        self.AppID = "******************"
        self.AK = "*******************"
        self.SK = "********************"
        self.host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(self.AK, self.SK)
        self.request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        self.access_token = requests.get(url=self.host).json()['access_token']

    def baidu_token_get(self):
        self.access_token = requests.get(self.host).json()['access_token']

    def ocr(self, img_bytes: io.BytesIO):
        img = img_bytes.getvalue()
        img = base64.b64encode(img)
        params = {"image": img}
        request_url = self.request_url + "?access_token=" + self.access_token
        response = requests.post(request_url, data=params, headers=self.headers)
        result = "".join([each['words'] + '\n' for each in response.json()['words_result']])
        return result


# Free BING API
# 注意, 这个API只能识别公式
# 不包含纯文本(会报错)
class Bing_LaTex_OCR:
    bing_url = 'http://www.bing.com/cameraexp/api/v1/getlatex'
    headers = {
        'Host': 'www.bing.com',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'User-Agent': 'Math/1 CFNetwork/1121.2.2 Darwin/19.3.0',
    }

    @staticmethod
    def bing_ocr(image_src: str, timeout=30):
        data = {'data': image_src,
                "inputForm": "Image",
                "clientInfo": {"app": "Math", "platform": "ios", "configuration": "Unknown", "version": "1.8.0",
                               "mkt": "zh-cn"}}
        rs = requests.post(Bing_LaTex_OCR.bing_url, headers=Bing_LaTex_OCR.headers, data=json.dumps(data))
        print(rs.json())
        return rs.json()

    @staticmethod
    def ocr(img_path):
        if type(img_path) is str:
            f = open(img_path, 'rb').read()
            img_data = base64.encodebytes(f).decode()
        elif type(img_path) is io.BytesIO:
            img_data = base64.encodebytes(img_path.getvalue()).decode()

        rs = Bing_LaTex_OCR.bing_ocr(img_data)
        if rs['isError']:
            return 0, None
        if not rs.get('latex'):
            return 1, rs.get('ocrText')
        else:
            return 1, rs['latex']



class Matpix_MyAccount:
    """
    My Matpix API hook
    can invite new email to obtain more
    """
    @staticmethod
    def image_uri(filename) -> str:
        """
        计算图片的URI
        :param filename:
        :return:
        """
        if type(filename) is str:
            image_data = open(filename, "rb").read()
        elif type(filename) is io.BytesIO:
            image_data = filename.getvalue()
            filename.close()
        return "data:image/jpeg;base64," + base64.encodebytes(image_data).decode()

    @staticmethod
    def matpix_ocr(image_src: str, timeout=30) -> Tuple[int, Any]:
        """
        :param image_src: 图片的URI
        :param timeout: 超时实践
        :return: [0, None] or [1, content]
        """
        url = 'https://api.mathpix.com/v1/snips'
        headers = {'Host': 'api.mathpix.com',
                   'Authorization': '*********************************************',
                   'User-Agent': 'Mathpix Snip Windows App v02.05.0009',
                   'Content-Type': 'application/json',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,en,*'
                   }
        payload = {
            "metadata": {
                "count": '292',
                "input_type": "crop",
                "platform": "windows 10",
                "skip_recrop": 'true',
                "user_id": "******************************",
                "version": "snip.windows@02.05.0009"
            },
            "src": image_src
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers,
                                 timeout=timeout).json()
        if response.get('latex'):
            return 1, response['latex']
        else:
            return 0, None

    @staticmethod
    def ocr(img_path):
        img_src = Matpix_MyAccount.image_uri(img_path)
        return Matpix_MyAccount.matpix_ocr(img_src)


class BaiduHandWritingOCR:
    AppID = "******"
    AK = "******************"
    SK = "******************"
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
        AK, SK)
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting"

    def __init__(self):
        self.access_token = requests.get(self.host).json()['access_token']

    def baidu_token_get(self):
        self.access_token = requests.get(self.host).json()['access_token']

    def ocr(self, img_bytes: io.BytesIO):
        img = base64.b64encode(img_bytes.getvalue())
        params = {"image": img}
        request_url = self.request_url + "?access_token=" + self.access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        result = "".join([each['words'] + '\n' for each in response.json()['words_result']])
        return result
