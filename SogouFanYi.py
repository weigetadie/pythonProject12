# 编程作者: WG
# 编程时间: 2023/6/17 20:29
"""
这是一个翻译程序,利用post请求爬取搜狗的翻译结果,本程序仅用于测试,不得用于商业目的.
因程序所引起的一切后果与本人无关

有问题可以联系作者..
                            ________.WG  QQ:459114916 (请注明来意)
"""
import json

import requests


class SogouFanYi(object):
    def __init__(self, content):

        self.url = "https://fanyi.sogou.com/api/transpc/text/transword"
        self.content = content

        self.headers = {

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.0.0',
            'Cookie': 'ABTEST=0|1682060927|v17; wuid=1682060927218; SUV=1682060928284; SGINPUT_UPSCREEN=1682060928295; FUV=15188e2314294629a087a81f6de7cff5; SNUID=B6D2F1CEE9EC17B8BA7E110AEA359129; SUID=5C3B1824BE55A00A00000000648DA50A; FQV=7859565c570f6aaee00110eae3a0abde; translate.sess=b9bc121a-834d-43eb-bb13-20ddbc3037dd'
        }

    def get_cookie(self):
        """
        发送数据包获取cookies
        :return:
        """
        # 这个是负载信息
        data = {'text': self.content}
        response = requests.post(self.url, data)
        cookie = response.cookies
        return cookie

    def set_transData(self):  # trans
        """
        设置负载(请求文本)
        :return: 返回data
        """

        # 向服务器发送post请求,以获取cookies
        # var = requests.post().cookies
        self.response = requests.post(self.url, headers=self.headers, json=self.data)
        print(self.response)

        if self.response.status_code == 200:
            # 解析响应数据，这里以 JSON 数据为例
            res = self.response.json()

            tgt_para = res["data"]['paraphrase'][0]['text']
            print(tgt_para)
            # # 获取"paraphrase"列表中的每个元素
            # paraphrases = res['data']['paraphrase'][0]['text']
            #
            # # 遍历每个元素获取"text"属性值
            # for paraphrase in paraphrases:
            #     text = paraphrase['text']
            #     print(text)


        else:
            print('请求失败，HTTP 状态码：', self.response.status_code)

    # 判断字符是否为汉字
    def is_chinese(self):
        sum = 0
        for char in self.content:

            if b'\xb0\xa1' <= char.encode('gb2312') <= b'\xd7\xf9':
                sum += 1

            else:
                sum -= 1
        if sum > 0:
            return True
        else:
            return False

    def run(self):
        data = {}
        if self.is_chinese():  # 这个是中文转英文
            data = {
                "from": "zh-CHS",
                "to": "en",
                "query": self.content
            }
            # 英文转中文
        else:
            data = {
                "from": "en",
                "to": "zh-CHS",
                "query": self.content
            }

        response = requests.post(self.url, headers=self.headers, data=data)
        print(response.text)

        # 将响应数据转换为 Python 字典
        data = response.json()

        # 获取 paraphrase 中 text 值的列表
        trans_text = data['data']['translation']['trans_text']

        # 打印 trans_text 值

        try:

            value = data['data']['paraphrase'][0]['value']

        except Exception:
            print(Exception.args)
            value = None
        finally:
            if value == None:
                print(trans_text)
                return trans_text
            else:
                print(trans_text)
                print(value)
                return trans_text + value


if __name__ == '__main__':
    while True:
        res = input('请输入翻译的内容:')
        js = SogouFanYi(res)
        print('翻译结果为: ', end="")
        js.run()
