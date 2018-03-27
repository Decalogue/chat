# Chat

`Chatbot based on natural language understanding and machine learning.`

`基于自然语言理解与机器学习的聊天机器人`

[![Documentation Status](https://readthedocs.org/projects/chat-cn/badge/?version=latest)](http://chat-cn.readthedocs.io/zh_CN/latest/?badge=latest)
[![PyPI Version](https://img.shields.io/pypi/v/chat.svg)](https://pypi.python.org/pypi/chat)

![chat](https://github.com/Decalogue/chat/blob/master/docs/img/chat.png "chat")

## 这就是 Chat

* Chat 是一个基于自然语言理解与机器学习的语义理解库。
* Chat 提供丰富的语义分析工具与语义知识图的构建工具，非常适合从0开始迅速搭建自己的聊天机器人，也能够减少工程师在实际开发当中的重复工作。
* Chat 非常易于修改和扩展，可以方便地个性化定制。如果您有如下需求，欢迎选择 Chat：
  
  * 想从0开始迅速搭建自己的聊天机器人
  * 想了解自然语言处理与机器学习算法在问答中的应用
  * 想智能化生活工作，提升效率
  * 对知识图谱以及 KBQA 感兴趣，想从0开始构建自己的知识图谱

> Chat适用的Python版本是：**Python 3.3-3.6**

## Installation 安装

    pip install --upgrade chat
    
## Tutorial 快速开始

### Step 1 在终端中启动数据库

> 方式1：直接使用 chat/tests/nlu.db 这个已经初始化的数据库
> 方式2：需自定义数据库，将其密码设为'train'
> 若要修改密码：可在 chat/conf/self.conf 中修改 [neo4j] 选项 password)

    neo4j start

### Step 2 初始化语义知识库

> 2.1 启动语义服务器并保持（详见 chat/tests/test_server.py，可命令行运行 python test_server.py）

    from chat import server
  
    server.start()
    
> 2.2 导入测试知识库（若直接使用 chat/tests/nlu.db 进入 Step 3）
> （详见 chat/tests/test_graph.py，可命令行运行 python test_graph.py）

    from chat.graph import Database
    
    kb = Database(password='train')
    kb.reset(filename='chat.xls') # 详见 chat/tests/chat.xls，可自定义问答
    
### Step 3 开始聊天

> 方式1：启动语义客户端
> （详见 chat/tests/test_client.py，可命令行运行 python test_client.py）

    from chat import client
  
    client.start()

> 方式2：使用 chat.qa 子模块

    from chat.qa import Robot
    from chat.config import getConfig
  
    robot = Robot(password=getConfig("neo4j", "password"))
    result = robot.search(question="您的自定义问题")
    answer = result['content']
    print(answer)


## Chat 的设计原则

* 用户友好：用户的使用体验始终是我们考虑的首要和中心内容。Chat 遵循减少认知困难的最佳实践：Chat 提供一致而简洁的 API， 能够极大减少一般应用下用户的工作量，同时，Chat 提供清晰和具有实践意义的 Bug 反馈。
* 模块性：完全独立可配置的模块可以用最少的代价自由组合在一起，您可以使用它们来构建自己的模块。
* 易扩展性：添加新模块超级容易，只需要仿照现有的模块编写新的类或函数即可。创建新模块的便利性使得 Chat 更适合于快速开发。
* 知识图谱：基于图数据库的知识图表达提供了更快的搜索速度与智能。

> 您可以在 [Read the docs](http://chat-cn.readthedocs.io/zh_CN/latest/) 中阅读官方中文文档。

> 如果您阅读在线中文文档时有什么问题，您可以在 Github 上下载这个项目，然后去 ***/docs/build/html/index.html*** 阅读离线中文文档。

`Copyright © 2017 Decalogue. All Rights Reserved.`

关于作者：[Decalogue](https://www.decalogue.cn)
