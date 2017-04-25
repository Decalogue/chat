#!/usr/bin/env python3
# -*- coding:utf8 -*-
# PEP 8 check with Pylint
"""Download knowledge base.
下载知识库。
"""

import sys
sys.path.append("../")
from chat.download import match

if __name__ == "__main__":
    match()
