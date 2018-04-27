# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from unittest import TestCase, main
from chat.semantic import synonym_cut, similarity, similarity2
from chat.mytools import time_me

class TestMe(TestCase):
    def setUp(self):
        pass

    @time_me()
    def test_similarity(self):
        data = [
            ("黄克功", "王怀安"),
            ("黄克功", "黄克功"),
            ("宋朝的历史", "明朝的历史"),
            ("电脑", "打印机"),
            ("怎么了？，。。。。", "怎么了?..,#$"),
            ("我喜欢你", "你喜欢我"),
            ("我要取票", "我要取票"),
            ("存钱", "取钱"),
            ("中国", "中华人民共和国"),
            ("喧闹的大街上人山人海", "热闹的街道上人来人往"),
            ("专心致志", "全神贯注"),
            ("爷爷爱吃土豆", "祖父喜欢吃马铃薯"),
            ("联想电脑多少钱", "联想笔记本价格"),
            ("今天天气怎么样", "我想去上海"),
            ("怎么花呗不能支付", "花呗付款不了怎么回事"),
            ("蚂蚁借呗的额度为什么会下降", "为什么借呗额度被降低了，没有不良记录"),
            ("蚂蚁借呗的额度为什么会下降", "为什么借呗额度被降低了"),
            ("花呗自动还款需要手续费ma", "花呗自动还款还要收手续费吗"),
            ("花呗怎么付款不鸟了", "帮忙看一下我花呗怎么用不了"),
            ("花呗被冻结怎么恢复", "花呗被封了怎么解除"),
            ("我借呗能不能开通", "如何开启借呗")
        ]
        for s1, s2 in data:      
            sv1 = synonym_cut(s1, 'wf')
            sv2 = synonym_cut(s2, 'wf')
            print(s1, 'VS', s2)
            print(sv1, 'VS', sv2)

            print("similarity1: ", similarity(sv1, sv2))
            print('similarity2: ', similarity2(s1, s2), '\n')


if __name__ == '__main__':
    main()
