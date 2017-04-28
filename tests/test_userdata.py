#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PEP 8 check with Pylint
"""Upload user data to graph from usb interface.
"""
import sys
sys.path.append("../")
from chat.database import Database
from chat.mytools import Walk

database = Database(password="train", userid="A0002")


class WalkUserData(Walk):
    def handle_file(self, filepath, pattern=None):
        database.handle_excel(filepath)

def add_excel(path=None, names=None):
    """Add subgraph from excel data.
    """
    walker = WalkUserData()
    fnamelist = walker.dir_process(1, path, style="fnamelist")

if __name__ == '__main__':
    add_excel("D:\新知识库")
