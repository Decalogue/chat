#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PEP 8 check with Pylint
"""Upload excel data to graph.
"""

from tkinter.filedialog import askopenfilename
from .database import Database

def add_excel(names=None):
    """Add subgraph from excel data.
    """
    database = Database(password="train")
    filename = askopenfilename(filetypes=[('QA的excel文档', '*.xls')])
    database.handle_excel(filename, custom_sheets=names)

def add_subgraph():
    """Add subgraph from other graph database.
    """
    pass

if __name__ == '__main__':
    add_excel()
    # add_subgraph()
