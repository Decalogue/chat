# -*- coding: utf-8 -*-
"""qa

QA based on NLU and Dialogue scene.
基于自然语言理解和对话场景的问答。

Available functions:
- All classes and functions: 所有类和函数
"""
import copy
import json
import sqlite3
from collections import deque
from py2neo import Graph, Node, Relationship, NodeSelector
from .config import getConfig
from .apilib import nlu_tuling, get_location_by_ip
from .semantic import synonym_cut, segment, get_tag, similarity, check_swords, get_location
from .mytools import time_me, get_current_time, random_item, get_age
from .word2pinyin import pinyin_cut, jaccard_pinyin

log_do_not_know = getConfig("path", "do_not_know")


# def get_navigation_location():
    # """获取导航地点 
    # """
    # try:
        # nav_db = getConfig("nav", "db")
        # tabel = getConfig("nav", "tabel")
        # conn = sqlite3.connect(nav_db)
    # except:
        # print("导航数据库连接失败！请检查是否存在文件：" + nav_db)
        # return []
    # try:
        # result = conn.execute("SELECT name from " + tabel)
    # except:
        # print("导航数据库没有找到表：" + tabel)
        # return []
    # names = [row[0] for row in result if row[0]]
    # return names


class Robot():
    """NLU Robot.
    自然语言理解机器人。

    Public attributes:
    - graph: The connection of graph database. 图数据库连接
    - selector: The selector of graph database. 图数据库选择器
    - locations: Navigation Locations. 导航地点列表
    - is_scene: 在线场景标志，默认为 False
    - user: 机器人配置信息
    - usertopics: 可用话题列表
    - address: 在线调用百度地图 IP 定位 API，网络异常时从配置信息获取默认地址
    - topic: 当前QA话题
    - qa_id: 当前QA id
    - qmemory: 短期记忆-最近用户问过的10个问题
    - amemory: 短期记忆-最近回答用户的10个答案
    - pmemory: 短期记忆-最近一次回答用户的正确答案
    - cmd_end_scene: 退出场景命令集
    - cmd_previous_step: 上一步命令集，场景内全局模式
    - cmd_next_step: 下一步命令集，通过界面按钮实现
    - cmd_repeat: 重复命令集
    - do_not_know: 匹配不到时随机回答
    """
    # userid="A0001" 为通用身份，可通过 self.init_user 设置自定义身份和挂接知识库
    def __init__(self, password="train", userid="A0001"):
        self.graph = Graph("http://localhost:7474/db/data/", password=password)
        self.selector = NodeSelector(self.graph)
        # self.locations = get_navigation_location()
        self.is_scene = False
        self.user = None
        # self.user = self.selector.select("User", userid=userid).first()
        # self.usertopics = self.get_usertopics(userid=userid)
        # self.address = get_location_by_ip(self.user['city'])
        self.topic = ""
        self.behavior = 0 # 场景类型 Add in 2018-6-7
        self.last_step_error = False # 在场景内上一个问答是否正常 Add in 2018-6-12
        self.qa_id = get_current_time()
        self.qmemory = deque(maxlen=10)
        self.amemory = deque(maxlen=10)
        self.pmemory = deque(maxlen=10)
        # TODO：判断意图是否在当前话题领域内
        self.change_attention = ["换个话题吧", "太无聊了", "没意思", "别说了"]
        self.cmd_end_scene = ["退出业务场景", "退出场景", "退出", "返回", "结束", "发挥"]
        self.cmd_previous_step = ["上一步", "上一部", "上一页", "上一个"]
        self.cmd_next_step = ["下一步", "下一部", "下一页", "下一个"]
        self.cmd_repeat = ["重复", "再来一个", "再来一遍", "你刚说什么", "再说一遍", "重来"]
        self.yes = ["是", "是的", "对", "对的", "好的", "YES", "yes", "结束了"]
        self.no = ["没", "没有", "否", "不", "没有结束", "没结束"]
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
        return "Hello! I'm {robotname} and I'm {robotage} years old.".format(**self.user)

    def init_user(self, userid=None, key=None):
        self.user = self.selector.select("User").where("_.userid='" + userid + "'", \
                    "_.key='" + key + "'").first()
        if self.user:
            self.usertopics = self.get_usertopics(userid=userid)
            self.address = get_location_by_ip(self.user['city'])

    @time_me()
    def configure(self, info="", userid="A0001", key="A0001"):
        """Configure knowledge base.
        配置知识库。
        """
        config = {"databases": []}
        # userid 不存在或者不正确时不能配置身份（通用身份只有管理员才能配置）
        if not self.user:
            self.init_user(userid, key)
        if not self.user:
            return config
        match_string = "MATCH (config:Config) RETURN config.name as name"
        subgraphs = [item[0] for item in self.graph.run(match_string)]
        print("所有知识库：", subgraphs)

        if info != '':
            selected_names = info.split()
            forbidden_names = list(set(subgraphs).difference(set(selected_names)))
            print("选中知识库：", selected_names)
            print("禁用知识库：", forbidden_names)
            # TODO：待合并精简 可用 CONTAINS
            for name in selected_names:
                match_string = "MATCH (user:User)-[r:has]->(config:Config) where user.userid='" \
                    + userid + "' AND config.name='" + name + "' SET r.bselected=1"
                self.graph.run(match_string)
            for name in forbidden_names:
                match_string = "MATCH (user:User)-[r:has]->(config:Config) where user.userid='" \
                    + userid + "' AND config.name='" + name + "' SET r.bselected=0"
                self.graph.run(match_string)

        match_string = "MATCH (user:User)-[r:has]->(config:Config)" + \
            "where user.userid='" + userid + \
            "' RETURN config.name as name, r.bselected as bselected, r.available as available"
        for item in self.graph.run(match_string):
            config["databases"].append(dict(name=item[0], bselected=item[1], available=item[2]))
        print("可配置信息：", config)
        
        return config

    # @time_me()
    def get_usertopics(self, userid="A0001"):
        """Get available topics list.
        """
        usertopics = []
        # userid 不存在或者不正确时使用通用身份
        if not userid:
            userid = "A0001"
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
        return sentence.format(**self.user)

    # @time_me()
    def add_to_memory(self, question="question", userid="A0001"):
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

    # def extract_navigation(self, question):
        """Extract navigation from question。从问题中抽取导航地点。
        从导航地点列表选取与问题匹配度最高的地点。
        QA匹配模式：（模糊匹配/全匹配）

        Args:
            question: User question. 用户问题。
        """
        # result = dict(question=question, name='', content=self.iformat(random_item(self.do_not_know)), \
            # context="", tid="", ftid="", url="", behavior=0, parameter="", txt="", img="", button="", valid=1)
        
        # 模式1：模糊匹配
        # temp_sim = 0
        # sv1 = synonym_cut(question, 'wf')
        # if not sv1:
            # return result
        # for location in self.locations:
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
        
        # 模式2：全匹配，判断“去”和地址关键词是就近的动词短语情况
        # for location in self.locations:
            
            # keyword = "去" + location
            # if keyword in question:
                # print("Original navigation")
                # result["name"] = keyword
                # result["content"] = location
                # result["context"] = "user_navigation"
                # result["behavior"] = int("0x001B", 16)
                # return result
        # return result

    def update_result(self, question='', node=None):
        result = dict(question=question, name='', content=self.iformat(random_item(self.do_not_know)), \
            context="", tid="", ftid="", url="", behavior=0, parameter="", txt="", img="", button="", valid=1)
        if not node:
            return result
        result['name'] = self.iformat(node["name"])
        result["content"] = self.iformat(random_item(node["content"].split("|")))
        result["context"] = node["topic"]
        result["tid"] = node["tid"]
        result["ftid"] = node["ftid"]
        result["txt"] = node["txt"]
        result["img"] = node["img"]
        result["button"] = node["button"]
        if node["url"]:
            result["url"] = random_item(node["url"].split("|"))
        if node["behavior"]:
            result["behavior"] = int(node["behavior"], 16)
        if node["parameter"]:
            result["parameter"] = node["parameter"]
        func = node["api"]
        if func:
            exec("result['content'] = " + func + "('" + result["content"] + "')")
        return result

    def extract_pinyin(self, question, subgraph, threshold=0.8, athreshold=0.9):
        """Extract synonymous QA in NLU database。
        QA匹配模式：从图形数据库选取匹配度最高的问答对。

        Args:
            question: User question. 用户问题。
            subgraph: Sub graphs corresponding to the current dialogue. 当前对话领域对应的子图。
        """
        temp_sim = 0
        ss = []
        max_score = 0
        sv1 = pinyin_cut(question)
        print(sv1)
        for node in subgraph:
            iquestion = self.iformat(node["name"])
            sv2 = pinyin_cut(iquestion)
            temp_sim = jaccard_pinyin(sv1, sv2)
            # 匹配加速，不必选取最高相似度，只要达到阈值就终止匹配
            if temp_sim > athreshold:
                print("Q: " + iquestion + " Similarity Score: " + str(temp_sim))
                return self.update_result(question, node)
        # ===========================================================
            ss.append(temp_sim)
        max_score = max(ss)
        if max_score > threshold:
            node = subgraph[ss.index(max_score)]
            iquestion = self.iformat(node["name"])
            print("Q: " + iquestion + " Similarity Score: " + str(max_score))
            return self.update_result(question, node)
        # ===========================================================
        return self.update_result(question)

    def extract_synonym(self, question, subgraph, threshold=0.60, athreshold=0.92):
        """Extract synonymous QA in NLU database。
        QA匹配模式：从知识库选取第一个超过匹配阈值的问答对。

        Args:
            question: User question. 用户问题。
            subgraph: Sub graphs corresponding to the current dialogue. 当前对话领域对应的子图。
        """
        temp_sim = 0
        ss = []
        max_score = 0
        sv1 = synonym_cut(question, 'wf') # 基于 semantic.jaccard
        # sv1 = segment(question) # 基于 semantic.jaccard2
        if not sv1:
            return self.update_result(question)
        for node in subgraph:
            iquestion = self.iformat(node["name"])
            if question == iquestion:
                print("Similarity Score: Original sentence")
                return self.update_result(question, node)
            sv2 = synonym_cut(iquestion, 'wf') # 基于 semantic.jaccard
            # sv2 = segment(iquestion) # 基于 semantic.jaccard2
            if sv2:
                temp_sim = similarity(sv1, sv2, 'j') # 基于 semantic.jaccard
                # temp_sim = similarity(sv1, sv2, 'j2') # 基于 semantic.jaccard2
            # 匹配加速，不必选取最高相似度，只要达到阈值就终止匹配
            if temp_sim > athreshold:
                print("Q: " + iquestion + " Similarity Score: " + str(temp_sim))
                return self.update_result(question, node)
        # ===========================================================
            ss.append(temp_sim)
        max_score = max(ss)
        if max_score > threshold:
            node = subgraph[ss.index(max_score)]
            iquestion = self.iformat(node["name"])
            print("Q: " + iquestion + " Similarity Score: " + str(max_score))
            return self.update_result(question, node)
        # ===========================================================
        return self.update_result(question)

    def extract_synonym_first(self, question, subgraph, threshold=0.60):
        """Extract synonymous QA in NLU database。
        QA匹配模式：从知识库选取匹配度最高的问答对。

        Args:
            question: User question. 用户问题。
            subgraph: Sub graphs corresponding to the current dialogue. 当前对话领域对应的子图。
        """
        temp_sim = 0
        ss = []
        max_score = 0
        sv1 = synonym_cut(question, 'wf') # 基于 semantic.jaccard
        # sv1 = segment(question) # 基于 semantic.jaccard2
        if not sv1:
            return self.update_result(question)
        for node in subgraph:
            iquestion = self.iformat(node["name"])
            if question == iquestion:
                print("Similarity Score: Original sentence")
                return self.update_result(question, node)
            sv2 = synonym_cut(iquestion, 'wf') # 基于 semantic.jaccard
            # sv2 = segment(iquestion) # 基于 semantic.jaccard2
            if sv2:
                temp_sim = similarity(sv1, sv2, 'j') # 基于 semantic.jaccard
                # temp_sim = similarity(sv1, sv2, 'j2') # 基于 semantic.jaccard2
            ss.append(temp_sim)
        max_score = max(ss)
        if max_score > threshold:
            node = subgraph[ss.index(max_score)]
            iquestion = self.iformat(node["name"])
            print("Q: " + iquestion + " Similarity Score: " + str(max_score))
            return self.update_result(question, node)
        return self.update_result(question)

    def extract_keysentence(self, question, data=None, threshold=0.40):
        """Extract keysentence QA in NLU database。
        QA匹配模式：从知识库选取包含关键句的问答对。

        Args:
            question: User question. 用户问题。
        """
        if data:
            subgraph = [node for node in data if node["name"] in question]
        else:
            usertopics = ' '.join(self.usertopics)
            # 只从目前挂接的知识库中匹配
            match_string = "MATCH (n:NluCell) WHERE '" + question + \
                "' CONTAINS n.name and '" + usertopics +  \
                "' CONTAINS n.topic RETURN n LIMIT 1"
            subgraph = [item['n'] for item in self.graph.run(match_string).data()]
        if subgraph:
            # 选取第一个匹配节点
            print("Similarity Score: Key sentence")
            # return self.extract_synonym(question, subgraph, threshold=threshold)
            node = subgraph[0]
            return self.update_result(question, node)
        return self.update_result(question)

    def extract_keysentence_first(self, question, data=None, threshold=0.40):
        """Extract keysentence QA in NLU database。
        QA匹配模式：从知识库选取包含关键句且匹配度最高的问答对。

        Args:
            question: User question. 用户问题。
        """
        if data:
            subgraph = [node for node in data if node["name"] in question]
        else:
            usertopics = ' '.join(self.usertopics)
            # 只从目前挂接的知识库中匹配
            match_string = "MATCH (n:NluCell) WHERE '" + question + \
                "' CONTAINS n.name and '" + usertopics +  \
                "' CONTAINS n.topic RETURN n"
            subdata = self.graph.run(match_string).data()
            subgraph = [item['n'] for item in subdata]
        if subgraph:
            # 选取得分最高的
            print("Similarity Score: Key sentence")
            return self.extract_synonym_first(question, subgraph, threshold=threshold)
        return self.update_result(question)

    def remove_name(self, question):
        # 姓氏误匹配重定义
        if question.startswith("小") and len(question) == 2:
            question = self.user['robotname']
        # 称呼过滤
        for robotname in ["小民", "小明", "小名", "晓明"]:
            if question.startswith(robotname) and len(question) >= 4 and "在线" not in question:
                question = question.lstrip(robotname)
        if not question:
            question = self.user['robotname']
        return question
    
    @time_me()
    def search(self, question="question", tid="", userid="A0001", key="A0001"):
        """Nlu search. 语义搜索。

        Args:
            question: 用户问题。
                Defaults to "question".
            userid: 用户唯一标识。
                Defaults to "userid"

        Returns:
            Dict contains:
            question, answer, topic, tid, url, behavior, parameter, txt, img, button.
            返回包含问题，答案，话题，资源，行为，动作，文本，图片及按钮的字典。
        """
        # 添加到问题记忆
        # self.qmemory.append(question)
        # self.add_to_memory(question, userid)

        # 语义：场景+全图+用户配置模式（用户根据 userid 动态获取其配置信息）
        # ========================初始化配置信息==========================
        if not self.user:
            self.init_user(userid, key)
        if not self.user:
            return dict(question=question, name="", content="身份验证失败", context="",\
                tid="", ftid="", url="", behavior=0, parameter="", txt="", img="", button="", valid=1)
        do_not_know = dict(
            question=question,
            name="",
            content=self.iformat(random_item(self.do_not_know)),
            context="",
            tid="",
            ftid="",
            url="",
            behavior=0,
            parameter="",
            txt="",
            img="",
            button="",
            valid=1)
        error_page = dict(
            question=question,
            name="",
            # content="这个业务办完了吗" # "这个问题结束了吗"
            content=self.user['error_page'],
            context="",
            tid="",
            ftid="",
            url="",
            behavior=int("0x1500", 16), # Modify：场景内 behavior 统一为 0x1500。(2018-1-8)
            parameter="",
            txt="",
            img="",
            button="",
            valid=0)

        # ========================一、预处理=============================
        # 敏感词过滤
        if check_swords(question):
            print("问题包含敏感词！")
            return do_not_know
        # 移除称呼
        question = self.remove_name(question)

        # ========================二、导航===============================
        # result = self.extract_navigation(question)
        # if result["context"] == "user_navigation":
            # self.amemory.append(result) # 添加到普通记忆
            # self.pmemory.append(result)
            # return result
        
        # ========================三、语义场景===========================
        result = copy.deepcopy(do_not_know)
        
        # 全局上下文——重复
        for item in self.cmd_repeat:
            # TODO：确认返回的是正确的指令而不是例如唱歌时的结束语“可以了”
            # TODO：从记忆里选取最近的有意义行为作为重复的内容
            if item == question:
                if self.amemory:
                    return self.amemory[-1]
                else:
                    return do_not_know

        # 场景——退出（通用）
        for item in self.cmd_end_scene:
            if item == question: # 完全匹配退出模式
                result['behavior'] = 0
                result['name'] = "退出"
                result['context'] = self.topic # Modify 2018-3-6 退出时返回的场景标签为当前场景
                result['content'] = ''
                self.is_scene = False
                self.topic = ''
                self.behavior = 0
                self.amemory.clear() # 清空场景记忆
                self.pmemory.clear() # 清空场景上一步记忆
                return result
        
        # 场景——意图跳转（多轮闲聊） Add in 2018-6-7
        if self.is_scene and self.behavior == 0:
            for item in self.change_attention:
                if item == question: # TODO：模糊匹配跳转模式
                    result['behavior'] = 0
                    result['name'] = "换个话题"
                    result['context'] = self.topic
                    result['content'] = "好的，我们换个话题吧"''
                    self.is_scene = False
                    self.topic = ''
                    self.amemory.clear() # 清空场景记忆
                    self.pmemory.clear() # 清空场景上一步记忆
                    return result

        # 场景——上一步：返回父节点(通用模式)
        if self.is_scene:
            for item in self.cmd_previous_step:
                if item in question:
                    # 添加了链接跳转判断（采用该方案 2017-12-22）
                    if len(self.pmemory) > 1:
                        self.amemory.pop()
                        return self.pmemory.pop()
                    elif len(self.pmemory) == 1:
                        return self.pmemory[-1]
                    else:
                        self.last_step_error = True
                        return error_page
            # 场景——下一步：通过 button 实现
            for item in self.cmd_next_step:
                if item in question:
                    if len(self.amemory) >= 1:
                        parent = self.amemory[-1]
                        if parent['button']:
                            next_name = parent['button'].split('|')[-1]
                            if next_name != '0': # 确定有下一步
                                # 下一步是当前场景节点的子节点
                                # match_string = "MATCH (n:NluCell {name:'" + \
                                    # next_name + "', topic:'" + self.topic + \
                                    # "', ftid:" + str(int(parent['tid'])) + "}) RETURN n"

                                # 下一步是当前场景节点的子节点或同层级节点 Modify：2018-2-26
                                match_string = "MATCH (n:NluCell) WHERE n.name='" + \
                                    next_name + "' and n.topic='" + self.topic + \
                                    "' and n.ftid IN [" + str(int(parent['tid'])) + \
                                    "," + str(int(parent['ftid'])) + "] RETURN n"

                                match_data = list(self.graph.run(match_string).data())                           
                                if match_data:
                                    node = match_data[0]['n']
                                    result = self.update_result(question, node)
                                    # 添加到场景记忆
                                    self.pmemory.append(self.amemory[-1])
                                    self.amemory.append(result)
                                    return result
                    self.last_step_error = True
                    return error_page
          
        # ==========================场景匹配=========================      
        if self.is_scene: # 在场景中：语义模式+关键句模式
            # 在场景内没有正确匹配时引导继续办理或者退出 Add in 2018-6-12
            if self.last_step_error:
                if question in self.yes:
                    result['behavior'] = 0
                    result['name'] = "退出"
                    result['context'] = self.topic
                    result['content'] = '好的，我们换个话题吧'
                    self.is_scene = False
                    self.topic = ''
                    self.behavior = 0
                    self.last_step_error = False
                    self.amemory.clear() # 清空场景记忆
                    self.pmemory.clear() # 清空场景上一步记忆
                    return result
                elif question in self.no:
                    result['behavior'] = self.behavior
                    result['name'] = "继续"
                    result['context'] = self.topic
                    if self.behavior == 0:
                        result['content'] = '好的'
                    else:
                        result['content'] = '请按屏幕提示操作继续业务哦'
                    self.last_step_error = False
                    return result
            # 场景内所有节点
            match_scene = "MATCH (n:NluCell) WHERE n.topic='" + self.topic + "' RETURN n"
            scene_nodes = self.graph.run(match_scene).data()
            # 根据场景节点的 ftid 是否等于父节点 tid 筛选子场景节点
            # subscene_nodes = [item['n'] for item in scene_nodes if item['n']['ftid'] == self.amemory[-1]['tid']]

            # 根据场景节点的 ftid 是否等于父节点 tid 或 ftid 筛选子场景节点及同层级节点 Modify：2018-2-26
            subscene_nodes = [item['n'] for item in scene_nodes
                if item['n']['ftid'] == self.amemory[-1]['tid'] or item['n']['ftid'] == self.amemory[-1]['ftid']]

            if subscene_nodes:
                result = self.extract_synonym_first(question, subscene_nodes)
                if not result["context"]:
                    result = self.extract_keysentence_first(question, subscene_nodes)
                if not result["context"]:
                    result = self.extract_pinyin(question, subscene_nodes)
                if result["context"]:
                    # print("正确匹配到当前场景的子场景")
                    print("正确匹配到当前场景的子场景或同层级场景") # Modify：2018-2-26
                    self.pmemory.append(self.amemory[-1])
                    self.amemory.append(result) # 添加到场景记忆
                    self.last_step_error = False
                    return result
            # 场景中匹配不到返回引导提示
            self.last_step_error = True
            return error_page
        else: # 不在场景中：语义模式+关键句模式
            # 和问题语义标签一致的所有节点
            tag = get_tag(question, self.user)
            match_graph = "MATCH (n:NluCell) WHERE n.tag='" + tag + \
                "' and '" + ' '.join(self.usertopics) + "' CONTAINS n.topic RETURN n"
            usergraph_all = [item['n'] for item in self.graph.run(match_graph).data()]
            if usergraph_all:
                # 同义句匹配 TODO：阈值可配置
                result = self.extract_synonym(question, usergraph_all, threshold=0.90)
                # 关键词匹配 TODO：配置开关
                if not result["context"]:
                    result = self.extract_keysentence(question)
                # 拼音匹配 TODO：配置开关
                if not result["context"]:
                    result = self.extract_pinyin(question, usergraph_all)
            # else: # 全局拼音匹配 TODO：配置开关
                # match_pinyin = "MATCH (n:NluCell) WHERE '" + \
                    # ' '.join(self.usertopics) + "' CONTAINS n.topic RETURN n"
                # usergraph_pinyin = [item['n'] for item in self.graph.run(match_pinyin).data()]
                # if usergraph_pinyin:
                    # result = self.extract_pinyin(question, usergraph_pinyin)
            if result["tid"] != '': # 匹配到场景节点
                if int(result["tid"]) == 0:
                    print("不在场景中，匹配到场景根节点")
                    self.is_scene = True # 进入场景
                    self.topic = result["context"]
                    # 场景类型 Add in 2018-6-7
                    self.behavior = result["behavior"]
                    self.last_step_error = False
                    self.amemory.clear() # 进入场景前清空普通记忆
                    self.pmemory.clear()
                    self.amemory.append(result) # 添加到场景记忆
                    self.pmemory.append(result)
                    return result
                else:
                    if result["behavior"] == 0: # Add in 2018-6-12
                        # 可以直接进入多轮闲聊子场景
                        print("不在场景中，匹配到闲聊场景子节点")
                        self.is_scene = True # 进入场景
                        self.topic = result["context"]
                        self.behavior = result["behavior"]
                        self.last_step_error = False
                        self.amemory.clear() # 进入场景前清空普通记忆
                        self.pmemory.clear()
                        self.amemory.append(result) # 添加到场景记忆
                        self.pmemory.append(result)
                        return result
                    else:
                        # 不可直接进入业务子场景
                        print("不在场景中，匹配到业务场景子节点")
                        return do_not_know
            elif result["context"]: # 匹配到普通节点
                self.topic = result["context"]
                self.amemory.append(result) # 添加到普通记忆
                self.pmemory.append(result)
                return result

        # ========五、在线语义（Modify：暂时关闭 2018-1-23）===============
        # if not self.topic:
            # 1.音乐(唱一首xxx的xxx)
            # if "唱一首" in question or "唱首" in question or "我想听" in question:
                # result["behavior"] = int("0x0001", 16)
                # result["content"] = "好的，正在准备哦"
            # 2.附近有什么好吃的
            # elif "附近" in question or "好吃的" in question:
                # result["behavior"] = int("0x001C", 16)
                # result["content"] = self.address
            # 3.nlu_tuling(天气)
            # elif "天气" in question:
                # 图灵API变更之后 Add in 2017-8-4
                # location = get_location(question)
                # if not location:
                    # 问句中不包含地址
                    # weather = nlu_tuling(self.address + question)
                # else:
                    # 问句中包含地址
                    # weather = nlu_tuling(question)
                # 图灵API变更之前    
                # weather = nlu_tuling(question, loc=self.address)
                # result["behavior"] = int("0x0000", 16)
                # try:
                    # 图灵API变更之前(目前可用)
                    # temp = weather.split(";")[0].split(",")[1].split()
                    # myweather = temp[0] + temp[2] + temp[3]

                    # 图灵API变更之后 Add in 2017-8-3
                    # temp = weather.split(",")
                    # myweather = temp[1] + temp[2]
                # except:
                    # myweather = weather
                # result["content"] = myweather
                # result["context"] = "nlu_tuling"
            # 4.追加记录回答不上的所有问题
            # else:
                # with open(log_do_not_know, "a", encoding="UTF-8") as file:
                    # file.write(question + "\n")
            # 5.nlu_tuling
            # else:
                # result["content"] = nlu_tuling(question, loc=self.address)
                # result["context"] = "nlu_tuling"
        # if result["context"]: # 匹配到在线语义
            # self.amemory.append(result) # 添加到普通记忆
        # ==============================================================
        
        # 追加记录回答不上的所有问题
        if not self.topic:
            with open(log_do_not_know, "a", encoding="UTF-8") as file:
                file.write(question + "\n")
        return result
