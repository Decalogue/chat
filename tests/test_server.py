#!/usr/bin/env python3
# -*- coding:utf8 -*-
# PEP 8 check with Pylint
"""server

Create and start NLU TCPServer with socketserver.
The socketserver module simplifies the task of writing network servers.
通过socketserver创建并启动语义理解服务器。
"""

import sys
sys.path.append("../")
from chat.server import start

if __name__ == "__main__":
    start()
	