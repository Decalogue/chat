# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from unittest import TestCase, main
from chat.client import start

class TestMe(TestCase):
    def setUp(self):
        self.userid = "A0003" # 智能客服：医院（名字：贝塔）
        self.key = "A0003"

    def test_start(self):
        start(userid=self.userid, key=self.key)


if __name__ == '__main__':
    main()
