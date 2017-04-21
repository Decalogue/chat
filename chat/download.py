#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter.filedialog import *
from .database import Database
from .mytools import write_excel

def match(*, label="NluCell", topic=""):
    database = Database(password="train")
    if topic:
        cypher_info = "MATCH (n:{label}) WHERE n.topic='{topic}' RETURN n"
    else:
        cypher_info = "MATCH (n:{label}) RETURN n"
    filename = asksaveasfilename(filetypes=[('QA的excel文档', '*.xls')])
    keys = ['name', 'content', 'topic', 'tag', 'keywords', 'api', 'behavior', 'url', "hot", 'txt', 'img', 'chart', 'parameter']
    # keys = database.graph.find_one(label).keys()
    items = database.graph.run(cypher_info.format(label=label, topic=topic)).data()
    sheets = [{"name": label, "keys": keys, "items": items}]
    write_excel(filename=filename, sheets=sheets)

if __name__ == '__main__':
    match(topic="")
