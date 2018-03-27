# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from unittest import TestCase, main
from chat.ianswer import answer2xml

class TestMe(TestCase):
    def setUp(self):
        pass

    def test_answer2xml(self):
        data = {
            'question': "看看理财产品", # 用户问题
            'content': "我行的各种理财产品请参考下图，您可以点击图标查看详情，也可以语音或手动选择购买。",
            'context': "理财产品",
            'url': "",
            'behavior': 5376, # 0x1500
            'parameter': '{"id": 1, "level": 3, "pos": 0.5}',
            'name': "理财产品", # 标准问题
            'tid': "0",
            'txt': "",
            'img': '[{"content": "乾元共享型理财产品", "iurl": "C:/nlu/data/img/1.png"}, {"content": "乾元周周利开放式保本理财产品", "iurl": "C:/nlu/data/img/2.png"}, {"content": "乾元私享型理财产品", "iurl": "C:/nlu/data/img/3.png"}, {"content": "乾元满溢120天开放式理财产品", "iurl": "C:/nlu/data/img/4.png"}]',
            'button': "0|手机银行办理|呼叫大堂经理|理财产品取号|乾元共享型理财产品",
            'valid': 1 # valid=0 代表 error_page
        }
        print(answer2xml(data))


if __name__ == '__main__':
    main()
