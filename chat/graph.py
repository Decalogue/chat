# -*- coding: utf-8 -*-
"""NLU Database Manager.
自然语言理解知识库管理。
"""
import os
import string
import xlwt
from collections import OrderedDict
from py2neo import Graph, Node, Relationship, NodeSelector
from tkinter.filedialog import askopenfilename
from .mytools import read_excel, write_excel, set_excel_style
from .semantic import get_tag


class Database():
    """Manage Database.
    管理数据库。

    Public attributes:
    - rdb: Relational database. 关系数据库。
    - graph: Graph database. 图数据库。
    """
    def __init__(self, password="train", userid="A0001"):
        self.rdb = None
        self.graph = Graph("http://localhost:7474/db/data", password=password)
        self.selector = NodeSelector(self.graph)
        self.user = self.selector.select("User", userid=userid).first()
        if not self.user:
            thispath = os.path.split(os.path.realpath(__file__))[0]
            with open(thispath + '/data/user.txt', 'r', encoding="UTF-8") as file:
                create_user = file.read()
            self.graph.run(create_user)
            self.user = self.selector.select("User", userid=userid).first()
        self.skb = ''
        self.dkb = []

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
            self.graph.run("MATCH (n)<-[r:" + label + "]-(m) DETACH DELETE r, n")
        elif pattern == "rm":
            self.graph.run("MATCH (n)-[r:" + label + "]->(m) DETACH DELETE r, m")
        elif pattern == "nrm":
            self.graph.run("MATCH (n)-[r:" + label + "]-(m) DETACH DELETE r, n, m")

    def reset(self, pattern="n", label="NluCell", filename=None):
        """Reset data of label in database.
        重置数据库子图。

        Args:
            pattern: Type of subgraph. 子图类型。
            label: Label of subgraph. 子图标签。
        """ 
        assert filename is not None, "filename can not be None."
        self.delete(pattern=pattern, label=label)
        print("Delete successfully!")
        if os.path.exists(filename):
            self.handle_excel(filename)
        else:
            print("You can set 'filename=<filepath>' when you call 'Database.reset.'")
        print("Reset successfully!")

    def reset_ts(self, pattern="n", label="TestStandard", filename=None):
        """Reset data of label in database.
        重置数据库子图。

        Args:
            pattern: Type of subgraph. 子图类型。
            label: Label of subgraph. 子图标签。
        """ 
        assert filename is not None, "filename can not be None."
        self.delete(pattern="n", label=label)
        print("Delete test standard successfully!")
        if os.path.exists(filename):
            self.handle_ts(filename)
        else:
            print("You can set 'filename=<filepath>' when you call 'Database.reset.'")
        print("Reset test standard successfully!")

    def add_nlucell(self, label="NluCell", name=None, content=None, topic="", tid="", \
        ftid="", behavior="", parameter="", url="", tag="", keywords="", api="", txt="", \
        img="", button="", description="", delimiter='|'):
        """Add nlucell node in graph.
        根据 name, topic, tid 确认节点是否已存在，存在则覆盖，不存在则追加。
        问题不能为空，避免因知识库表格填写格式不对而导致存入空问答对
        """
        assert name is not None, "name must be string."
        assert content is not None, "content must be string."
        for question in name.split(delimiter):
            question = question.strip()
            if question: # 问题不能为空
                # 根据 name, topic, tid 确认节点是否已存在
                match_tid = "''" if tid == '' else str(tid)
                node = self.selector.select("NluCell").where("_.name ='" + question + "'", \
                    "_.topic ='" + topic + "'", "_.tid =" + match_tid).first()
                if node: # 存在则覆盖
                    # node['name'] = question
                    node['content'] = content
                    # node['topic'] = topic
                    # node['tid'] = tid
                    node['ftid'] = ftid
                    node['behavior'] = behavior
                    node['parameter'] = parameter
                    node['url'] = url
                    # node['tag'] = tag
                    node['keywords'] = keywords
                    node['api'] = api
                    node['txt'] = txt
                    node['img'] = img
                    node['button'] = button
                    node['description'] = description
                    self.graph.push(node)
                else: # 不存在则追加
                    tag = get_tag(question, self.user)
                    node = Node(label, name=question, content=content, topic=topic, \
                        tid=tid, ftid=ftid, behavior=behavior, parameter=parameter, \
                        url=url, tag=tag, keywords=keywords, api=api, txt=txt, img=img, \
                        button=button, description=description, hot=0)
                    self.graph.create(node)

    def add_ts(self, label="TestStandard", question=None, content=None, context="", \
    behavior="", parameter="", url=""):
        """
        Add test standard node in graph.
        """
        assert question is not None, "question must be string."
        assert content is not None, "content must be string."
        for item in question.split():
            item = item.strip()
            if item: # 问题不能为空，避免因知识库表格填写格式不对而导致存入空问答对
                node = Node(label, question=item, content=content, context=context, \
                behavior=behavior, parameter=parameter, url=url)
                self.graph.create(node)

    def handle_ts(self, filename=None, custom_sheets=[]):
        """Processing data of test standard.
        """
        assert filename is not None, "filename can not be None."
        data = read_excel(filename)
        data_sheets = data.sheet_names()
        if custom_sheets:
            sheet_names = list(set(data_sheets).intersection(set(custom_sheets)))
        else:
            sheet_names = data_sheets
        for sheet_name in sheet_names: # 可自定义要导入的子表格
            table = data.sheet_by_name(sheet_name)
            # 1.Select specified table
            # table = data.sheet_by_index(0)
            if table:
                # 2.Select specified column
                col_format = ['A', 'B', 'C', 'D', 'E', 'F']
                try:
                    nrows = table.nrows
                    # ncols = table.ncols
                    str_upcase = [i for i in string.ascii_uppercase]
                    i_upcase = range(len(str_upcase))
                    ncols_dir = dict(zip(str_upcase, i_upcase))
                    col_index = [ncols_dir.get(i) for i in col_format]
                    # 前两行为表头
                    for i in range(2, nrows):
                        question = table.cell(i, col_index[0]).value
                        content = table.cell(i, col_index[1]).value
                        context = table.cell(i, col_index[2]).value
                        behavior = table.cell(i, col_index[3]).value
                        parameter = table.cell(i, col_index[4]).value
                        url = table.cell(i, col_index[5]).value
                        self.add_ts(question=question, content=content, context=context, \
                        behavior=behavior, parameter=parameter, url=url)
                except Exception as error:
                    print('Error: %s' %error)
                    return None
            else:
                print('Error! Data of %s is empty!' %sheet_name)
                return None

    def handle_excel(self, filename=None, custom_sheets=[]):
        """Processing data of excel.
        """
        assert filename is not None, "filename can not be None"
        data = read_excel(filename)
        data_sheets = data.sheet_names()
        if custom_sheets: # 可自定义要导入的子表格
            sheet_names = list(set(data_sheets).intersection(set(custom_sheets)))
        else:
            sheet_names = data_sheets
        for sheet_name in sheet_names:
            table = data.sheet_by_name(sheet_name)
            topics = []
            # 1.Select specified table
            # table = data.sheet_by_index(0)
            if table:
                # 2.Select specified column
                col_format = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
                try:
                    nrows = table.nrows
                    # ncols = table.ncols
                    str_upcase = [i for i in string.ascii_uppercase]
                    i_upcase = range(len(str_upcase))
                    ncols_dir = dict(zip(str_upcase, i_upcase))
                    col_index = [ncols_dir.get(i) for i in col_format]
                    # 前两行为表头，从第3行开始读取
                    for i in range(2, nrows):
                        name = table.cell(i, col_index[0]).value
                        content = table.cell(i, col_index[1]).value
                        # Modify：2018-1-17
                        # 场景 topic 必须填写，问答 topic 可不填，若填写必须为 sheet_name
                        temp = table.cell(i, col_index[2]).value
                        topic =  temp if temp else sheet_name
                        
                        temp = table.cell(i, col_index[3]).value
                        tid = int(temp) if temp != '' else ''
                        
                        temp = table.cell(i, col_index[4]).value
                        ftid = int(temp) if temp != '' else ''
                        
                        behavior = table.cell(i, col_index[5]).value
                        parameter = table.cell(i, col_index[6]).value
                        url = table.cell(i, col_index[7]).value
                        tag = table.cell(i, col_index[8]).value
                        keywords = table.cell(i, col_index[9]).value
                        api = table.cell(i, col_index[10]).value
                        txt = table.cell(i, col_index[11]).value
                        img = table.cell(i, col_index[12]).value
                        button = table.cell(i, col_index[13]).value
                        description = table.cell(i, col_index[14]).value
                        # hot = 0 table.cell(i, col_index[15]).value
					    # 3.Your processing function of excel data here                           
                        self.add_nlucell(name=name, content=content, topic=topic, \
                            tid=tid, ftid=ftid, behavior=behavior, parameter=parameter, \
                            url=url, tag=tag, keywords=keywords, api=api, txt=txt, \
                            img=img, button=button, description=description, delimiter="|")
                        # 添加到场景标签列表
                        if topic:
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
                # 默认 self.user 已存在
                self.graph.run('MATCH (user:User {userid: "' + self.user["userid"] + \
                '"})\nCREATE (config:Config {name: "' + sheet_name + '", topic: "' + \
                ",".join(set(topics)) + '"})\nCREATE (user)-[:has {bselected: 1, available: 1}]->(config)')
            else:
                # 追加并更新可用话题集
                alltopics = config_node["topic"].split(",") if config_node["topic"] else []
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
                self.add_nlucell(name=question, content=answer, delimiter="|")
                question = file.readline().rstrip()

    def get_available_kb(self):
        kb = []
        match_str = "MATCH (user:User {userid: '" + self.user['userid'] + "'})\
            -[r:has {available:1}]->(config:Config) RETURN config.name as name"
        for item in self.graph.run(match_str):
            kb.append(item['name'])
        return kb
    
    def get_selected_kb(self):
        kb = []
        match_str = "MATCH (user:User {userid: '" + self.user['userid'] + "'})\
            -[r:has {bselected:1, available:1}]->(config:Config) RETURN config.name as name"
        for item in self.graph.run(match_str):
            kb.append(item['name'])
        return kb

    def download(self, filename=None, names=[]):
        """下载知识库
        """
        assert filename is not None, "Filename must be *.xls!"
        assert names is not [], "Subgraph names can not be empty!"
        cypher_info = "MATCH (n:NluCell) WHERE n.topic='{topic}' RETURN n"
        # Modify：使键值按照指定顺序导出 excel (2018-1-8)
        info = [('name', '问题'), ('content', '回答'), ('topic', '场景标签'), ('tid', '场景ID'),
            ('ftid', '父场景ID'), ('behavior', '行为'), ('parameter', '动作参数'), ('url', '资源'), 
            ('tag', '语义标签'), ('keywords', '关键词'), ('api', '内置功能'), ('txt', '显示文本'), 
            ('img', '显示图片'), ('button', '显示按钮'), ('description', '场景描述'), ("hot", '搜索热度')]
        # Modify：若采用字典，可用如下方案(2018-1-9)
        # import collections
        # info = collections.OrderedDict(info)
        sheets = []
        
        for name in names:
            subgraph = self.selector.select('Config', name=name).first()
            topics = subgraph["topic"].split(",") if subgraph else []
            items = []
            for topic in topics:
                match_str = cypher_info.format(topic=topic)
                item = list(self.graph.run(match_str).data())
                items.extend(item)
            sheets.append({"name": name, "info": info, "items": items})
            
        write_excel(filename=filename, sheets=sheets)
        
    def download_scene(self, label="NluCell", filename=None, topic=''):
        """Match scene and download.
        """
        assert filename is not None, "Filename must be *.xls!"
        assert topic is not '', "Topic can not be ''!"
        info = [('name', '问题'), ('content', '回答'), ('topic', '场景标签'), ('tid', '场景ID'),
            ('ftid', '父场景ID'), ('behavior', '行为'), ('parameter', '动作参数'), ('url', '资源'), 
            ('tag', '语义标签'), ('keywords', '关键词'), ('api', '内置功能'), ('txt', '显示文本'), 
            ('img', '显示图片'), ('button', '显示按钮'), ('description', '场景描述'), ("hot", '搜索热度')]
        cypher_info = "MATCH (n:{label}) WHERE n.topic='{topic}' RETURN n"
        match_str = cypher_info.format(label=label, topic=topic)
        
        config_info = "MATCH (n:Config) WHERE n.topic contains '{topic}' RETURN n.name as name"
        config = self.graph.run(config_info.format(topic=topic)).data()
        name = list(config)[0]['name'] if config else "业务场景"
        
        items = list(self.graph.run(match_str).data())
        sheets = [{"name": name, "info": info, "items": items}]
        write_excel(filename=filename, sheets=sheets)
    
    def upload(self, pattern='qa', names=[]):
        """上传知识库
        """
        if pattern == 'qa':
            filename = askopenfilename(filetypes=[('QA', '*.xls')])
            self.handle_excel(filename, custom_sheets=names)
        elif pattern == 'ts':
            filename = askopenfilename(filetypes=[('测试标准', '*.xls')])
            self.handle_ts(filename, custom_sheets=names)

    def generate_testcases(self, *, filename=None, custom_sheets=None, savedir='.'):
        """Generating test cases from data of excel.
        
        custom_sheets 选择的子表格集合
        """
        assert filename is not None, "filename can not be None"
        data = read_excel(filename) # 读取已有excel-知识库
        data_sheets = data.sheet_names()
        if custom_sheets:
            sheet_names = list(set(data_sheets).intersection(set(custom_sheets)))
        else:
            sheet_names = data_sheets
            
        file = xlwt.Workbook() # 创建新excel-测试用例
        new_sheet = file.add_sheet("NluTest", cell_overwrite_ok=True) # 创建sheet
        keys = ["问题", "答案", "是否通过", "改进建议"]
        # 生成表头
        new_sheet.write(0, 0, "本地语义常见命令问答测试", set_excel_style('Arial Black', 220, True))
        for col, key in enumerate(keys):
            new_sheet.write(1, col, key, set_excel_style('Arial Black', 220, True))
        count = 0
        testlist = []
        # 生成内容       
        for sheet_name in sheet_names:
            table = data.sheet_by_name(sheet_name)
            # 1.Select specified table
            # table = data.sheet_by_index(0)
            if data:
                # 2.Select specified column
                col_format = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
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
                        questions = name.format(**self.user).split("|")
                        answers = content.format(**self.user).split("|")
                        testlist.extend(questions)
                        new_sheet.write(i+count, 0, "\n".join(questions))
                        new_sheet.write(i+count, 1, "\n".join(answers))
                    count += nrows - 2
                except Exception as error:
                    print('Error: %s' %error)
                    return None
            else:
                print('Error! Data of %s is empty!' %sheet_name)
                return None
        file.save(savedir + "/testcase.xls") # 保存文件
        with open(savedir + "/testcase.txt", 'w', encoding="UTF-8") as newfile:
            for item in testlist:
                newfile.write(item + "\n")
