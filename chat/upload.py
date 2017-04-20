#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from database import Database
from tkinter.filedialog import *

def add_excel():
    database = Database(password="train")
    filename = askopenfilename(filetypes=[('QA的excel文档', '*.xls')])
    database.handle_excel(filename)
    
def add_subgraph(names=None):
    assert names is not None, "subgraph names can not be None"
    database = Database(password="train")
    names = ["基础问答", "基础_银行"]
    database.handle_excel(filename="C:/nlu/data/chat.xls", custom_sheets=names)

if __name__ == '__main__':
    add_excel()
    # add_subgraph()
