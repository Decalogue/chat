#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PEP 8 check with Pylint
"""Manage NLU database based on neo4j graph database.
管理基于neo4j图形数据库的自然语言理解数据库。

The 'py2neo' is a python package of neo4j graph database.
1.Support increase, delete, modify, query and other operations for nodes,
relationships, subgraph and graph;
2.Support batch processing;
3.Support command line;
4.Support read the data file, batch import and export.
"py2neo"是neo4j图形数据库的python接口包。
1.支持节点，关系，子图，全图的增、删、改、查；
2.支持批处理；
3.支持命令行；
4.支持读取数据文件批量导入及导出。

Available functions:
- All classes and functions: 所有类和函数
"""
import string
from optparse import OptionParser
from py2neo import Graph, Node, Relationship, NodeSelector
from .mytools import read_excel
from .semantic import get_tag


class Database():
    """Manage Database.
    管理数据库。

    It support python command line parameter processing of relational database
    and graph database.
    You can view all the features by 'python xxx.py -h'.
    支持关系数据库和图形数据库的python命令行参数处理。
    可以通过'python xxx.py -h'查看所有功能。

    Public attributes:
    - rdb: Relational database. 关系数据库。
    - graph: Graph database. 图数据库。
    """
    def __init__(self, password=None, userid="userid"):
        self.rdb = None
        self.graph = Graph("http://localhost:7474/db/data", password=password)
        self.gconfig = self.graph.find_one("User", "userid", userid)
        self.selector = NodeSelector(self.graph)
        self.usage = "usage: python %prog [options] arg"
        self.version = "%prog 1.0"
        self.parser = OptionParser(usage=self.usage, version=self.version)
        self.parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
        self.parser.add_option("-q", "--quiet", action="store_false", dest="verbose")
        self.parser.add_option("-b", "--batch", dest="batch", action="store_true", \
        help="batch processing of graph database")
        self.parser.add_option("-f", "--file", dest="filename", \
        help="read data from filename")
        self.parser.add_option("-p", "--path", dest="filepath", \
        help="read data from filepath")
        self.parser.add_option("-a", "--add", dest="add", \
        help="add subgraph to graph database")
        self.parser.add_option("-d", "--delete", dest="delete", \
        help="delete subgraph of graph database")
        self.parser.add_option("-e", "--edit", dest="edit", \
        help="edit subgraph of graph database")
        self.parser.add_option("-s", "--search", dest="search", \
        help="search subgraph of graph database")
        (self.options, self.args) = self.parser.parse_args()
        # if len(self.args) == 0:
            # self.parser.error("incorrect number of arguments")
        if self.options.verbose:
            print("reading %s..." % self.options.filename)
        if self.options.delete:
            for name in self.args:
                self.delete(pattern=self.options.delete, name=name)

    def delete(self, pattern="n", name=None):
        """Batch delete data or subgraph in database.
        在数据库中批量删除数据或者子图。

        Args:
            pattern: Type of subgraph. 子图类型。
            name: Name of subgraph. 子图名称。
        """
        if pattern == "all":
            self.graph.delete_all()
        elif pattern == "n":
            self.graph.run("MATCH(n:" + name + ") DETACH DELETE n")
        elif pattern == "r":
            self.graph.run("MATCH (n)-[r:" + name + "]-(m) DETACH DELETE r")
        elif pattern == "nr":
            self.graph.run("MATCH (n)<-[r:" + name + "]-(m) DETACH DELETE r DELETE n")
        elif pattern == "rm":
            self.graph.run("MATCH (n)-[r:" + name + "]->(m) DETACH DELETE r DELETE m")
        elif pattern == "nrm":
            self.graph.run("MATCH (n)-[r:" + name + "]-(m) DETACH DELETE r DELETE n DELETE m")

    def add_qa(self, nodeclass="NluCell", name=None, content=None, topic="", \
    behavior="", parameter="", url="", tag="", keywords="", api="", txt="", \
    img="", chart="", delimiter=None):
        """
        Add qa node in graph.
        """
        assert name is not None, "name must be string."
        assert content is not None, "content must be string."
        questions = name.split(delimiter)
        for question in questions:
            tag = get_tag(question, self.gconfig)
            node = Node(nodeclass, name=question, content=content, topic=topic, \
            behavior=behavior, parameter=parameter, url=url, tag=tag, \
            keywords=keywords, api=api, txt=txt, img=img, chart=chart, hot="0")
            self.graph.create(node)

    def handle_excel(self, filename=None, custom_sheets=None):
        """Processing data of excel.
        """
        assert filename is not None, "filename can not be None"
        data = read_excel(filename)
        data_sheets = data.sheet_names()
        if custom_sheets:
            sheet_names = list(set(data_sheets).intersection(set(custom_sheets)))
        else:
            sheet_names = data_sheets
        for sheet_name in sheet_names: # 可自定义要导入的子表格
            table = data.sheet_by_name(sheet_name)
            topics = []
            # 1.Select specified table
            # table = data.sheet_by_index(0)
            if data:
                # 2.Select specified column
                col_format = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
                try:
                    nrows = table.nrows
                    # ncols = table.ncols
                    str_upcase = [i for i in string.ascii_uppercase]
                    i_upcase = range(len(str_upcase))
                    ncols_dir = dict(zip(str_upcase, i_upcase))
                    col_index = [ncols_dir.get(i) for i in col_format]
                    # 前两行为表头
                    for i in range(2, nrows):
                        name = table.cell(i, col_index[0]).value
                        content = table.cell(i, col_index[1]).value
                        topic = table.cell(i, col_index[2]).value
                        behavior = table.cell(i, col_index[3]).value
                        parameter = table.cell(i, col_index[4]).value
                        url = table.cell(i, col_index[5]).value
                        tag = table.cell(i, col_index[6]).value
                        keywords = table.cell(i, col_index[7]).value
                        api = table.cell(i, col_index[8]).value
                        txt = table.cell(i, col_index[9]).value
                        img = table.cell(i, col_index[10]).value
                        chart = table.cell(i, col_index[11]).value
                        # hot = 0 table.cell(i, col_index[12]).value
					    # 3.Your processing function of excel data here
                        self.add_qa(name=name, content=content, topic=topic, \
                        behavior=behavior, parameter=parameter, url=url, tag=tag, \
                        keywords=keywords, api=api, txt=txt, img=img, chart=chart, \
                        delimiter="|")
                        # 添加到场景标签列表
                        topics.append(topic)
                except Exception as error:
                    print('Error: %s' %error)
                    return None
            else:
                print('Error! Data of %s is empty!' %sheet_name)
                return None
            # Modify in 2017.4.28
            # 若子表格名字不存在，新建配置子图，否则只修改topic属性
            config_node = self.graph.find_one("Config", "name", sheet_name)
            if not config_node:
                self.graph.run('MATCH (user:User {userid: "' + self.gconfig["userid"] + \
                '"})\nCREATE (config:Config {name: "' + sheet_name + '", topic: "' + \
                ",".join(set(topics)) + '"})\nCREATE (user)-[:has {bselected: 1, available: 1}]->(config)')
            else:
                alltopics = config_node["topic"].split(",")
                alltopics.extend(topics)
                config_node["topic"] = ",".join(set(alltopics))
                self.graph.push(config_node)

    def handle_txt(self, filename=None):
        """
        Processing text file to generate subgraph.
        """
        assert filename is not None, "filename can not be None"
        with open(filename, encoding="UTF-8") as file:
            question = file.readline().rstrip()
            while question:
                answer = file.readline().rstrip()
                print("question: " + question)
                print("answer: " + answer)
                self.add_qa(name=question, content=answer, delimiter="|")
                question = file.readline().rstrip()
