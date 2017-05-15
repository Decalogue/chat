#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PEP 8 check with Pylint
"""Reset local semantic database. 重置本地语义知识库。
"""

from .database import Database

def reset_nlucell():
    """Reset data of label 'NluCell' in database.
    """
    database = Database(password="train")
    database.delete(pattern="n", name="NluCell")
    print("Delete successfully!")
    # 知识库excel 文件路径待定
    # 方案1：固定路径如"C:/nlu/data/chat.xls"，需要每次拷贝；
    # 方案2：和chat一起打包分发，包含在"C:\\Program Files (x86)\\Anaconda3\\Lib\\site-packages\\chat\\data目录中；
    # 方案3：自动从git远程拉取。
    filename = "C:/nlu/data/chat.xls"
    database.handle_excel(filename)
    print("Reset successfully!")

if __name__ == '__main__':
    reset_nlucell()
