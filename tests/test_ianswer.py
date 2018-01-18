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
            'behavior': 4098, # 0x1002
            'parameter': "{'id': 1, 'level': 3, 'pos': 0.5}",
            'name': "理财产品", # 标准问题
            'tid': "0",
            'txt': "",
            'img': '{"area_1": {"pos": 1, "content": "乾元共享型理财产品", "iurl": "img/1.jpg", "url": "1"}, "area_2": {"pos": 2, "content": "乾元周周利开放式保本理财产品", "iurl": "img/2.jpg", "url": "2"}, "area_3": {"pos": 3, "content": "乾元私享型理财产品", "iurl": "img/3.jpg", "url": "3"}, "area_4": {"pos": 4, "content": "乾元满溢120天开放式理财产品", "iurl": "img/4.jpg", "url": "4"}}',
            'button': '{"previous": {"pos": 0, "content": "理财产品", "url": "0"}, "next": {"pos": 4, "content": "乾元共享型理财产品", "url": "1"},"area": {"area_1": {"pos": 1, "content": "手机银行办理", "url": "5"}, "area_2": {"pos": 2, "content": "呼叫大堂经理", "url": "6"}, "area_3": {"pos": 3, "content": "理财产品取号", "url": "7"}}}',
            'valid': 1 # valid=0 代表 error_page
        }
        print(answer2xml(data))


if __name__ == '__main__':
    main()
