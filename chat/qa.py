#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PEP 8 check with Pylint
"""qa

NLU based on Natural Language Processing and Graph Database.
基于自然语言处理与图形数据库的自然语言理解。

Available functions:
- All classes and functions: 所有类和函数
"""
import sqlite3
from collections import deque
from concurrent.futures import ProcessPoolExecutor
from py2neo import Graph, Node, Relationship
from .api import nlu_tuling, get_location_by_ip
from .semantic import synonym_cut, get_tag, similarity, check_swords
from .mytools import time_me, get_current_time, random_item

# 获取导航地点——Development requirements from Mr Tang in 2017-5-11.
def get_navigation_location():
    db = sqlite3.connect("C:/docu/db/contentDB.db")
    cursor = db.execute("SELECT name from goalvoice")
    # 过滤0记录
    names = [row[0] for row in cursor if row[0]]
    return names

class Robot():
    """NLU Robot.
    自然语言理解机器人。

    Public attributes:
    - graph: The connection of graph database. 图形数据库连接。
    - pattern: The pattern for NLU tool: 'semantic' or 'vec'. 语义标签或词向量模式。
    - memory: The context memory of robot. 机器人对话上下文记忆。
    """
    def __init__(self, password="train"):
        # 连接图知识库
        self.graph = Graph("http://localhost:7474/db/data/", password=password)
        # 语义模式：'semantic' or 'vec'
        self.pattern = 'semantic'
        # 获取导航地点数据库
        self.locations = get_navigation_location()
        # 在线场景标志，默认为False
        self.is_scene = False
        # 在线调用百度地图IP定位api，网络异常时返回默认地址：上海市
        self.address = get_location_by_ip()
        # 机器人配置信息
        self.gconfig = None
        # 可用话题列表
        self.usertopics = []
        # 当前QA话题
        self.topic = ""
        # 当前QA id
        self.qa_id = get_current_time()
		# 短期记忆：最近问过的10个问题与10个答案
        self.qmemory = deque(maxlen=10)
        self.amemory = deque(maxlen=10)
        # 匹配不到时随机回答
        self.do_not_know = [
            "这个问题太难了，{robotname}还在学习中",
            "这个问题{robotname}不会，要么我去问下",
            "您刚才说的是什么，可以再重复一遍吗",
            "{robotname}刚才走神了，一不小心没听清",
            "{robotname}理解的不是很清楚啦，你就换种方式表达呗",
            "不如我们换个话题吧",
            "咱们聊点别的吧",
            "{robotname}正在学习中",
            "{robotname}正在学习哦",
            "不好意思请问您可以再说一次吗",
            "额，这个问题嘛。。。",
            "{robotname}得好好想一想呢",
            "请问您说什么",
            "您问的问题好有深度呀",
            "{robotname}没有听明白，您能再说一遍吗"
        ]

    def __str__(self):
        return "Hello! I'm {robotname} and I'm {robotage} years old.".format(**self.gconfig)

    @time_me()
    def configure(self, info="", userid="userid"):
        """Configure knowledge base.
        配置知识库。
        """
        assert userid is not "", "The userid can not be empty!"
        # TO UPGRADE 对传入的userid参数分析，若不合适则报相应消息 2017-6-7
        if userid != "A0001":
            userid = "A0001"
            print("userid 不是标准A0001，已经更改为A0001")
        match_string = "MATCH (config:Config) RETURN config.name as name"
        subgraphs = [item[0] for item in self.graph.run(match_string)]
        print("所有知识库：", subgraphs)
        if not info:
            config = {"databases": []}
            match_string = "MATCH (user:User)-[r:has]->(config:Config)" + \
                "where user.userid='" + userid + \
                "' RETURN config.name as name, r.bselected as bselected, r.available as available"
            for item in self.graph.run(match_string):
                config["databases"].append(dict(name=item[0], bselected=item[1], available=item[2]))
            print("可配置信息：", config)
            return config
        else:
            selected_names = info.split()
        forbidden_names = list(set(subgraphs).difference(set(selected_names)))
        print("选中知识库：", selected_names)
        print("禁用知识库：", forbidden_names)
        # TODO：待合并精简
        for name in selected_names:
            match_string = "MATCH (user:User)-[r:has]->(config:Config) where user.userid='" \
                + userid + "' AND config.name='" + name + "' SET r.bselected=1"
            # print(match_string)
            self.graph.run(match_string)
        for name in forbidden_names:
            match_string = "MATCH (user:User)-[r:has]->(config:Config) where user.userid='" \
                + userid + "' AND config.name='" + name + "' SET r.bselected=0"
            # print(match_string)
            self.graph.run(match_string)
        return self.get_usertopics(userid=userid)

    # @time_me()
    def get_usertopics(self, userid="userid"):
        """Get usertopics list.
        """
        usertopics = []
        if not userid:
            userid = "userid"
        # 从知识库获取用户拥有权限的子知识库列表
        match_string = "MATCH (user:User)-[r:has {bselected:1, available:1}]->(config:Config)" + \
            "where user.userid='" + userid + "' RETURN config"
        data = self.graph.run(match_string).data()
        for item in data:
            usertopics.extend(item["config"]["topic"].split(","))
        print("用户：", userid, "\n已有知识库列表：", usertopics)
        return usertopics

    def iformat(self, sentence):
        """Individualization of robot answer.
        个性化机器人回答。
        """
        return sentence.format(**self.gconfig)

    # @time_me()
    def add_to_memory(self, question="question", userid="userid"):
        """Add user question to memory.
        将用户当前对话加入信息记忆。

        Args:
            question: 用户问题。
                Defaults to "question".
            userid: 用户唯一标识。
                Defaults to "userid".
        """
        previous_node = self.graph.find_one("Memory", "qa_id", self.qa_id)
        self.qa_id = get_current_time()
        node = Node("Memory", question=question, userid=userid, qa_id=self.qa_id)
        if previous_node:
            relation = Relationship(previous_node, "next", node)
            self.graph.create(relation)
        else:
            self.graph.create(node)

    # Development requirements from Mr Tang in 2017-5-11.
    # 由模糊匹配->全匹配 from Mr Tang in 2017-6-1.
    def extract_navigation(self, question):
        """Extract navigation。抽取导航地点。
        QA匹配模式：从导航地点列表选取匹配度最高的地点。

        Args:
            question: User question. 用户问题。
        """
        result = dict(question=question, content=self.iformat(random_item(self.do_not_know)), \
            context="", url="", behavior=0, parameter=0)
        # temp_sim = 0
        # sv1 = synonym_cut(question, 'wf')
        # if not sv1:
            # return result
        for location in self.locations:
            if "去" in question and location in question:
                print("Original navigation")
                result["content"] = location
                result["context"] = "user_navigation"
                result["behavior"] = int("0x001B", 16)
                return result
            # sv2 = synonym_cut(location, 'wf')
            # if sv2:
                # temp_sim = similarity(sv1, sv2, 'j')
            # 匹配加速，不必选取最高相似度，只要达到阈值就终止匹配
            # if temp_sim > 0.92:
                # print("Navigation location: " + location + " Similarity Score: " + str(temp_sim))
                # result["content"] = location
                # result["context"] = "user_navigation"
                # result["behavior"] = int("0x001B", 16)
                # return result
        return result

    def extract_synonym(self, question, subgraph):
        """Extract synonymous QA in NLU database。
        QA匹配模式：从图形数据库选取匹配度最高的问答对。

        Args:
            question: User question. 用户问题。
            subgraph: Sub graphs corresponding to the current dialogue. 当前对话领域对应的子图。
        """
        temp_sim = 0
        result = dict(question=question, content=self.iformat(random_item(self.do_not_know)), \
            context="", url="", behavior=0, parameter=0)
	    # semantic: 切分为同义词标签向量，根据标签相似性计算相似度矩阵，由相似性矩阵计算句子相似度
	    # vec: 切分为词向量，根据word2vec计算相似度矩阵，由相似性矩阵计算句子相似度
        if self.pattern == 'semantic':
        # elif self.pattern == 'vec':
            sv1 = synonym_cut(question, 'wf')
            if not sv1:
                return result
            for node in subgraph:
                iquestion = self.iformat(node["name"])
                if question == iquestion:
                    print("Similarity Score: Original sentence")
                    result["content"] = self.iformat(random_item(node["content"].split("|")))
                    result["context"] = node["topic"]
                    if node["url"]:
                        # result["url"] = json.loads(random_item(node["url"].split("|")))
                        result["url"] = random_item(node["url"].split("|"))
                    if node["behavior"]:
                        result["behavior"] = int(node["behavior"], 16)
                    if node["parameter"]:
                        result["parameter"] = int(node["parameter"])
                    # 知识实体节点api抽取原始问题中的关键信息，据此本地查询/在线调用第三方api/在线爬取
                    func = node["api"]
                    if func:
                        exec("result['content'] = " + func + "('" + result["content"] + \
                            "', " + "question)")
                    return result
                sv2 = synonym_cut(iquestion, 'wf')
                if sv2:
                    temp_sim = similarity(sv1, sv2, 'j')
			    # 匹配加速，不必选取最高相似度，只要达到阈值就终止匹配
                if temp_sim > 0.92:
                    print("Q: " + iquestion + " Similarity Score: " + str(temp_sim))
                    result["content"] = self.iformat(random_item(node["content"].split("|")))
                    result["context"] = node["topic"]
                    if node["url"]:
                        # result["url"] = json.loads(random_item(node["url"].split("|")))
                        result["url"] = random_item(node["url"].split("|"))
                    if node["behavior"]:
                        result["behavior"] = int(node["behavior"], 16)
                    if node["parameter"]:
                        result["parameter"] = int(node["parameter"])
                    func = node["api"]
                    if func:
                        exec("result['content'] = " + func + "('" + result["content"] + \
                            "', " + "question)")
                    return result
        return result

    @time_me()
    def search(self, question="question", userid="userid"):
        """Nlu search. 语义搜索。

        Args:
            question: 用户问题。
                Defaults to "question".
            userid: 用户唯一标识。
                Defaults to "userid"

        Returns:
            Dict contains answer, current topic, url, behavior and parameter.
            返回包含答案，当前话题，资源包，行为指令及对应参数的字典。
        """
        # 添加到问题记忆
        # self.qmemory.append(question)
        # self.add_to_memory(question, userid)

        # 本地语义：全图模式
        #tag = get_tag(question)
        #subgraph = self.graph.find("NluCell", "tag", tag)
        #result = self.extract_synonym(question, subgraph)

        # 本地语义：场景+全图+用户配置模式
        # 多用户根据userid动态获取对应的配置信息
        self.gconfig = self.graph.find_one("User", "userid", userid)
        self.usertopics = self.get_usertopics(userid=userid)

        # 问题过滤器(添加敏感词过滤 2017-5-25)
        if check_swords(question):
            print("问题包含敏感词！")
            return dict(question=question, content=self.iformat(random_item(self.do_not_know)), \
            context="", url="", behavior=0, parameter=0)

        # 导航: Development requirements from Mr Tang in 2017-5-11.
        result = self.extract_navigation(question)
        if result["context"] == "user_navigation":
            return result

        # 云端在线场景
        result = dict(question=question, content="ok", context="basic_cmd", url="", \
        behavior=int("0x0000", 16), parameter=0)
        # TODO: 简化为统一模式
        # TODO {'behavior': 0, 'content': '理财产品取号', 'context': 'basic_cmd', 'parameter': 0, 'question': '理财产品取号', 'url': ''}
        if "理财产品" in question and "取号" not in question:
            result["behavior"] = int("0x1002", 16) # 进入在线场景
            result["question"] = "理财产品" # 重定义为标准问题
            self.is_scene = True # 在线场景标志
        if "免费wifi" in question or "wifi" in question:
            result["behavior"] = int("0x1002", 16) # 进入在线场景
            result["question"] = "有没有免费的wifi" # 重定义为标准问题
            self.is_scene = True # 在线场景标志
        if "存款利率" in question:
            result["behavior"] = int("0x1002", 16) # 进入在线场景
            result["question"] = "存款利率" # 重定义为标准问题
            self.is_scene = True # 在线场景标志
        if "我要取钱" in question or "取钱" in question:
            result["behavior"] = int("0x1002", 16) # 进入在线场景
            result["question"] = "我要取钱" # 重定义为标准问题
            self.is_scene = True # 在线场景标志
        if "信用卡挂失" in question:
            result["behavior"] = int("0x1002", 16) # 进入在线场景
            result["question"] = "信用卡挂失" # 重定义为标准问题
            self.is_scene = True # 在线场景标志
        if "开通云闪付" in question:
            result["behavior"] = int("0x1002", 16) # 进入在线场景
            result["question"] = "开通云闪付" # 重定义为标准问题
            self.is_scene = True # 在线场景标志
        if "办理粤卡通" in question or "办理粤通卡" in question:
            result["behavior"] = int("0x1002", 16) # 进入在线场景
            result["question"] = "办理粤卡通" # 重定义为标准问题
            self.is_scene = True # 在线场景标志
        # 进入在线场景
        # start_scene = ["理财产品", "wifi", "存款利率", "取钱", "信用卡挂失", "开通云闪付", "办理粤卡通"]
        # for item in start_scene:
            # if item in question:
                # result["behavior"] = int("0x1002", 16) # 进入在线场景
                # result["question"] = "办理粤卡通" # 重定义为标准问题
                # self.is_scene = True # 在线场景标志
        # 退出在线场景
        end_scene = ["退出业务场景", "退出", "返回", "结束", "发挥"]
        for item in end_scene:
            if item in question:
                result["behavior"] = int("0x0020", 16) # 场景退出
                self.is_scene = False
                return result
        previous_step = ["上一步", "上一部", "上一页", "上一个"]
        next_step = ["下一步", "下一部", "下一页", "下一个"]
        if self.is_scene:
            # for item in previous_step:
                # if item in question:
                    # result["behavior"] = int("0x001D", 16) # 场景上一步
            # for item in next_step:
                # if item in question:
                    # result["behavior"] = int("0x001E", 16) # 场景下一步
            if "上一步" in question or "上一部" in question or "上一页" in question or "上一个" in question:
                result["behavior"] = int("0x001D", 16) # 场景上一步
            elif "下一步" in question or "下一部" in question or "下一页" in question or "下一个" in question:
                result["behavior"] = int("0x001E", 16) # 场景下一步
            result["content"] = question
            return result

        # 常用命令，交互，业务
        # 上下文——重复命令 TODO：确认返回的是正确的指令而不是例如唱歌时的结束语“可以了”
        if "再来一个" in question:
            # TODO：从记忆里选取最近的有意义行为作为重复的内容
            return self.amemory[-1]
        # 本地标准语义
        tag = get_tag(question, self.gconfig)
        subgraph_all = list(self.graph.find("NluCell", "tag", tag))
        # subgraph_scene = [node for node in subgraph_all if node["topic"]==self.topic]
        usergraph_all = [node for node in subgraph_all if node["topic"] in self.usertopics]
        usergraph_scene = [node for node in usergraph_all if node["topic"] == self.topic]
        # if subgraph_scene:
        if usergraph_scene:
            result = self.extract_synonym(question, usergraph_scene)
            if result["context"]:
                self.topic = result["context"]
                self.amemory.append(result) # 添加到答案记忆
                return result
        result = self.extract_synonym(question, usergraph_all)
        # result  = self.extract_synonym(question, subgraph_all)
        self.topic = result["context"]
        self.amemory.append(result) # 添加到答案记忆

        # 在线语义
        if not self.topic:
            # TODO：待完善的姓名不匹配问题
            if question.startswith("我叫"):
                result["behavior"] = int("0x000A", 16)
                result["content"] = "3,2,1，茄子"
                result["context"] = "basic_cmd"
            # 1.音乐(唱一首xxx的xxx)
            elif "唱一首" in question or "唱首" in question or "我想听" in question:
                result["behavior"] = int("0x0001", 16)
                result["content"] = "好的，正在准备哦"
            # 2.附近有什么好吃的
            elif "附近" in question or "好吃的" in question:
                result["behavior"] = int("0x001C", 16)
                result["content"] = self.address
            # 3.nlu_tuling(天气) TO Upgrade
            elif "天气" in question:
                weather = nlu_tuling(question, loc=self.address)
                result["behavior"] = int("0x0000", 16)
                temp = weather.split(";")[0].split(",")[1].split()
                result["content"] = temp[0] + temp[2] + temp[3]
                result["context"] = "nlu_tuling"
            # 4.nlu_tuling
            # else:
                # result["content"] = nlu_tuling(question, loc=self.address)
                # result["context"] = "nlu_tuling"
        return result
