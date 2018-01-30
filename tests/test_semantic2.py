# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from unittest import TestCase, main
from chat.semantic2 import similarity

class TestMe(TestCase):
    def setUp(self):
        pass

    def test_similarity(self):
        data = [
            ('小民', '小民'),
            ("电脑", "打印机"),
            ("电脑", "笔记本"),
            ("怎么了？，。。。。", "怎么了?..,#$"),
            ("我喜欢你", "你喜欢我"),
            ("我要取票", "我要取票"),
            ("存钱", "取钱"),
            ("中国", "中华人民共和国"),
            ("喧闹的大街上人山人海", "热闹的街道上人来人往"),
            ("专心致志", "全神贯注"),
            ("爷爷爱吃土豆", "祖父喜欢吃马铃薯"),
            ("联想电脑多少钱", "联想笔记本价格"),
            ("今天天气怎么样", "我想去上海")
        ]
        for s1, s2 in data:
            print(s1, ' vs ', s2)
            print('score: ', similarity(s1, s2), '\n')


if __name__ == '__main__':
    main()
