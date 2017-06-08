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
import os
import string
from optparse import OptionParser
from py2neo import Graph, Node, Relationship, NodeSelector
from .mytools import read_excel
from .semantic import get_tag

# Add in 2017-5-12 知识库excel文件路径
datapath = os.path.split(os.path.realpath(__file__))[0]


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
    def __init__(self, password="train", userid="userid", is_admin=True):
        self.is_admin = is_admin
        self.rdb = None
        self.graph = Graph("http://localhost:7474/db/data", password=password)
        self.selector = NodeSelector(self.graph)
        # DeprecationWarning: Graph.find_one is deprecated, use NodeSelector instead. 2017-5-18
        # self.gconfig = self.graph.find_one("User", "userid", userid)
        # 用法1：subgraph = selector.select("Label", property=value)
        # 用法2：subgraph = selector.select("Person").where("_.name =~ 'J.*'", "1960 <= _.born < 1970")
        self.gconfig = self.selector.select("User", userid=userid).first()
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
            for label in self.args:
                self.delete(pattern=self.options.delete, label=label)

    def delete(self, pattern="n", label=None):
        """Batch delete data or subgraph in database.
        在数据库中批量删除数据或者子图。

        Args:
            pattern: Type of subgraph. 子图类型。
            label: Label of subgraph. 子图标签。
        """
        if pattern == "all":
            self.graph.delete_all()
        elif pattern == "n":
            self.graph.run("MATCH(n:" + label + ") DETACH DELETE n")
        elif pattern == "r":
            self.graph.run("MATCH (n)-[r:" + label + "]-(m) DETACH DELETE r")
        elif pattern == "nr":
            self.graph.run("MATCH (n)<-[r:" + label + "]-(m) DETACH DELETE r DELETE n")
        elif pattern == "rm":
            self.graph.run("MATCH (n)-[r:" + label + "]->(m) DETACH DELETE r DELETE m")
        elif pattern == "nrm":
            self.graph.run("MATCH (n)-[r:" + label + "]-(m) DETACH DELETE r DELETE n DELETE m")

    def reset(self, pattern="n", label=None, filename=None):
        """Reset data of label in database.
        重置数据库子图。

        Args:
            pattern: Type of subgraph. 子图类型。
            label: Label of subgraph. 子图标签。
        """ 
        self.delete(pattern="n", label="NluCell")
        print("Delete successfully!")
        if os.path.exists(filename):
            self.handle_excel(filename)
        else:
            print("You can set 'filename=<filepath>' when you call 'Database.reset.'")
        print("Reset successfully!")

    def add_qa(self, label="NluCell", name=None, content=None, topic="", \
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
            node = Node(label, name=question, content=content, topic=topic, \
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
                        # TODO 确定用户可以自定义哪些内容
                        topic = table.cell(i, col_index[2]).value if self.is_admin else "user_chat"
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
            # DeprecationWarning: Graph.find_one is deprecated, use NodeSelector instead. 2017-5-18
            # config_node = self.graph.find_one("Config", "name", sheet_name)
            config_node = self.selector.select("Config", name=sheet_name).first()
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
        assert filename is not None, "filename can not be None!"
        with open(filename, encoding="UTF-8") as file:
            question = file.readline().rstrip()
            while question:
                answer = file.readline().rstrip()
                print("question: " + question)
                print("answer: " + answer)
                self.add_qa(name=question, content=answer, delimiter="|")
                question = file.readline().rstrip()

    def register_subgraph(self, *, label="Config", name=None, topic=None):
        """注册子知识库
        """
        assert name is not None, "Subgraph name can not be None!"
        assert topic is not None, "Subgraph topic can not be None!"
        subgraph = self.selector.select(label, name=name).first()
        if subgraph:
            topics = subgraph["topic"].split(",")
            topics.extend(topic.split(","))
            subgraph["topic"] = ",".join(set(topics))
            self.graph.push(subgraph)
        else:
            node = Node(label, name=name, topic=topic)
            self.graph.create(node)

    def register_user(self, *, label="User", profile=None):
        """注册用户
        """
        userid = input("\n欢迎注册！请输入userid: ")
        while not userid:
            userid = input("userid不能为空！请输入userid: ")
        while self.graph.run("MATCH (user:User {userid: '" + userid + "'}) RETURN user").data():
            userid = input("用户已存在！请输入新的userid: ")
        username = input("username: ")
        robotname = input("robotname: ")
        robotage = input("robotage: ")
        robotgender = input("robotgender: ")
        mother = input("mother: ")
        father = input("father: ")
        companyname = input("companyname: ")
        companytype = input("companytype: ")
        servicename = input("servicename: ")
        director = input("director: ")
        address = input("address: ")
        province = input("province: ")
        city = input("city: ")
        node = Node(label, userid=userid, username=username, robotname=robotname, \
        robotage=robotage, robotgender=robotgender, mother=mother, father=father, \
        companyname=companyname, companytype=companytype, servicename=servicename, \
        director=director, address=address, province=province, city=city)
        self.graph.create(node)
        print("注册成功！")
        # 设置知识库权限
        subgraph_names = [item["name"] for item in self.selector.select("Config")]
        print("可配置知识库列表：", subgraph_names)
        for name in subgraph_names:
            self.manage_user(userid=userid, name=name)

    def manage_user(self, *, userid=None, name=None):
        """管理用户
        """
        assert userid is not None, "Userid can not be None!"
        assert name is not None, "Subgraph name can not be None!"
        user = self.selector.select("User", userid=userid).first()
        if not user:
            print("用户不存在，建议您先注册！")
            return
        subgraph = self.selector.select("Config", name=name).first()
        if not subgraph:
            print("知识库不存在，建议您先注册！")
            return

        print("\n待配置知识库：", name)
        bselected = input("是否选择 [1/0]: ")
        if not bselected: bselected = "1"
        available = input("是否可用 [1/0]: ")
        if not available: available = "1"
        set_string = "MATCH (user:User {userid: '" + userid + "'}), (subgraph:Config {name: '" \
        + name + "'}) CREATE UNIQUE (user)-[r:has]->(subgraph) SET r.bselected=" \
        + bselected + ", r.available=" + available
        self.graph.run(set_string)
        # match_string = "MATCH (user:User {userid: '" + userid + \
        # "'})-[r:has]->(subgraph:Config {name: '" + name +"'}) RETURN r"
        # relation = self.graph.run(match_string).data()
        # if relation: # set
            # set_string = "MATCH (user:User {userid: '" + userid + \
        # "'})-[r:has]->(subgraph:Config {name: '" + name +"'}) SET r.bselected=" + bselected +", r.available=" + available
            # self.graph.run(set_string)
        # else: # create
            # create_string = "MATCH (user:User {userid: '" + userid + \
            # "'}), (subgraph:Config {name: '" + name +"'})" + \
            # " CREATE UNIQUE (user)-[:has {bselected: " + bselected + \
            # ", available: " + available + "}]->(subgraph)"
            # self.graph.run(create_string)
