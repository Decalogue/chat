# -*- coding:utf8 -*-
"""kmapi

Create and start KB Manager Server.
创建并启动语义知识库管理服务器。
"""
import sys
sys.path.append("../")
from unittest import TestCase, main
from chat.kmapi import start

class TestMe(TestCase):
    def setUp(self):
        pass
        
    def test_start(self):
        start()

if __name__ == '__main__':
    main()
