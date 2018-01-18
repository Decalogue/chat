#!/usr/bin/env python3
# -*- coding:utf8 -*-
# PEP 8 check with Pylint
"""Download knowledge base.
下载知识库。
"""

import sys
sys.path.append("../")
from chat.database import Database

if __name__ == "__main__":
    database = Database(password="train", userid="A0001")
    database.download(filename="test.xls", names=['业务场景', '问答'])
    database.download_scene(filename="scene.xls", topic='financial_products')
