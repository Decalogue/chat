# -*- coding:utf8 -*-
"""server

Create and start NLU TCPServer.
创建并启动语义理解服务器。
"""
import sys
sys.path.append("../")
from unittest import TestCase, main
from chat.server import start

class TestMe(TestCase):
    def setUp(self):
        pass
        
    def test_start(self):
        start()

if __name__ == '__main__':
    main()
