import re

import execjs
import requests


class Translator:
    ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072;       
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f";    
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
      };      
      function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
      } 
     """)
    sign = execjs.compile("""function a(r, o) {
    for (var t = 0; t < o.length - 2; t += 3) {
        var a = o.charAt(t + 2);
        a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
        a = "+" === o.charAt(t + 1) ? r >>> a: r << a,
        r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
    }
    return r
}
var C = null;
var token = function(r, _gtk) {
    var o = r.length;
    o > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(o / 2) - 5, 10) + r.substring(r.length, r.length - 10));
    var t = void 0,
    t = null !== C ? C: (C = _gtk || "") || "";
    for (var e = t.split("."), h = Number(e[0]) || 0, i = Number(e[1]) || 0, d = [], f = 0, g = 0; g < r.length; g++) {
        var m = r.charCodeAt(g);
        128 > m ? d[f++] = m: (2048 > m ? d[f++] = m >> 6 | 192 : (55296 === (64512 & m) && g + 1 < r.length && 56320 === (64512 & r.charCodeAt(g + 1)) ? (m = 65536 + ((1023 & m) << 10) + (1023 & r.charCodeAt(++g)), d[f++] = m >> 18 | 240, d[f++] = m >> 12 & 63 | 128) : d[f++] = m >> 12 | 224, d[f++] = m >> 6 & 63 | 128), d[f++] = 63 & m | 128)
    }
    for (var S = h,
    u = "+-a^+6",
    l = "+-3^+b+-f",
    s = 0; s < d.length; s++) S += d[s],
    S = a(S, u);

    return S = a(S, l),
    S ^= i,
    0 > S && (S = (2147483647 & S) + 2147483648),
    S %= 1e6,
    S.toString() + "." + (S ^ h)
}
    """)

    @staticmethod
    def get_google_token(text: str):
        return Translator.ctx.call("TL", text)

    @staticmethod
    def translate_using_google(string: str):
        tk = Translator.get_google_token(string)
        assert type(string) == str
        param = {'tk': tk, 'q': string}
        result = requests.get("""http://translate.google.cn/translate_a/single?client=t&sl=en
                  &tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss
                  &dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2""", params=param)
        translated_data = ""
        for each in result.json()[0]:
            if each[0] is None:
                continue
            else:
                translated_data += each[0]
        return translated_data

    @staticmethod
    def translate_using_youdao(string: str):
        url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
        data = {'i': string,
                'from': 'en',
                'to': 'zh-CHS',
                'smartresult': 'dict',
                'client': 'fanyideskweb',
                'doctype': 'json',
                'version': '2.1',
                'keyfrom': 'fanyi.web',
                'action': 'FY_BY_REALTlME',
                'typoResult': 'false'}
        result = requests.post(url, data=data).json()
        translated_data = ""
        for sentence in result['translateResult']:
            for each in sentence:
                translated_data += each['tgt']
                translated_data += "\n"
        return translated_data

    class BaiduTranslator:
        def __init__(self):
            self.sess = requests.Session()
            self.headers = {
                'User-Agent':
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
            }
            self.token = None
            self.gtk = None

            # 获得token和gtk
            # 必须要加载两次保证token是最新的，否则会出现998的错误
            self.loadMainPage()
            self.loadMainPage()

        def loadMainPage(self):
            """
                load main page : https://fanyi.baidu.com/
                and get token, gtk
            """
            url = 'https://fanyi.baidu.com'

            try:
                r = self.sess.get(url, headers=self.headers)
                self.token = re.findall(r"token: '(.*?)',", r.text)[0]
                self.gtk = re.findall(r"window.gtk = '(.*?)';", r.text)[0]
            except Exception as e:
                raise e
                # print(e)

        def langdetect(self, query):
            """
                post query to https://fanyi.baidu.com/langdetect
                return json
                {"error":0,"msg":"success","lan":"en"}
            """
            url = 'https://fanyi.baidu.com/langdetect'
            data = {'query': query}
            try:
                r = self.sess.post(url=url, data=data)
            except Exception as e:
                raise e
                # print(e)

            json = r.json()
            if 'msg' in json and json['msg'] == 'success':
                return json['lan']
            return None

        def dictionary(self, query):
            """
                max query count = 2
                get translate result from https://fanyi.baidu.com/v2transapi
            """
            url = 'https://fanyi.baidu.com/v2transapi'

            sign = Translator.sign.call('token', query, self.gtk)

            lang = self.langdetect(query)
            data = {
                'from': 'en' if lang == 'en' else 'zh',
                'to': 'zh' if lang == 'en' else 'en',
                'query': query,
                'simple_means_flag': 3,
                'sign': sign,
                'token': self.token,
            }
            try:
                r = self.sess.post(url=url, data=data)
            except Exception as e:
                raise e

            if r.status_code == 200:
                json = r.json()
                if 'error' in json:
                    raise Exception('baidu sdk error: {}'.format(json['error']))
                    # 998错误则意味需要重新加载主页获取新的token
                return json
            return None

        def dictionary_by_lang(self, query, fromlang, tolang):
            """
                max query count = 2
                get translate result from https://fanyi.baidu.com/v2transapi
            """
            url = 'https://fanyi.baidu.com/v2transapi'

            sign = Translator.sign.call('token', query, self.gtk)

            data = {
                'from': fromlang,
                'to': tolang,
                'query': query,
                'simple_means_flag': 3,
                'sign': sign,
                'token': self.token,
            }
            try:
                r = self.sess.post(url=url, data=data)
            except Exception as e:
                raise e
            result = ""
            if r.status_code == 200:
                json = r.json()
                if 'error' in json:
                    raise Exception('baidu sdk error: {}'.format(json['error']))
                    # 998错误则意味需要重新加载主页获取新的token
                # print(json["trans_result"]["data"])
                for each in json["trans_result"]["data"]:
                    result += each['dst']
                    result += "\n"
                return result
            return None

        def get_dict_result(self, query):
            r = self.dictionary(query)
            try:
                r = r['dict_result']['simple_means']['word_means']
                return r
            except Exception as e:
                return ['']