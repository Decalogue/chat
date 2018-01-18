# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from unittest import TestCase, main
from chat.semantic import synonym_cut, similarity

class TestMe(TestCase):
    def setUp(self):
        pass

    def test_similarity(self):
        data = [
            ("中国", "中华人民共和国"),
            ("喧闹的大街上人山人海", "热闹的街道上人来人往"),
            ("专心致志", "全神贯注"),
            ("爷爷爱吃土豆", "祖父喜欢吃马铃薯"),
            ("联想电脑多少钱", "联想笔记本价格"),
            ("今天天气怎么样", "我想去上海")
        ]
        for sentence1, sentence2 in data:
            sv1 = synonym_cut(sentence1, 'wf')
            sv2 = synonym_cut(sentence2, 'wf')
            print(sentence1, sv1)
            print(sentence2, sv2)
            sim = similarity(sv1, sv2)
            print("words similarity: ", str(sim), '\n')


if __name__ == '__main__':
    main()
