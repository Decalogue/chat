.. _tutorial:

======================
快速开始 QA
======================

Step 1 在终端中启动数据库
-----------------------------

* 方式1：直接使用 chat/tests/nlu.db 这个已经初始化的数据库

* 方式2：需自定义数据库，将其密码设为'train'

* 若要修改密码：可在 chat/conf/self.conf 中修改 [neo4j] 选项 password)

.. code-block:: bash
  
  neo4j start

Step 2 初始化语义知识库
-----------------------------

* 2.1 启动语义服务器并保持（详见 chat/tests/test_server.py，可命令行运行 python test_server.py）

.. code-block:: python

  from chat import server
  
  server.start()
  
* 2.2 导入测试知识库（若直接使用 chat/tests/nlu.db 进入 Step 3）

（详见 chat/tests/test_graph.py，可命令行运行 python test_graph.py）

.. code-block:: python

  from chat.graph import Database
    
  kb = Database(password='train')
  kb.reset(filename='chat.xls') # 详见 chat/tests/chat.xls，可自定义问答
  
Step 3 开始聊天
-----------------------------

* 方式1：启动语义客户端

（详见 chat/tests/test_client.py，可命令行运行 python test_client.py）

.. code-block:: python

  from chat import client
  
  client.start()
  
* 方式2：使用 chat.qa 子模块

.. code-block:: python

  from chat.qa import Robot
  from chat.config import getConfig
  
  robot = Robot(password=getConfig("neo4j", "password"))
  result = robot.search(question="您的自定义问题")
  answer = result['content']
  print(answer)
  
配置 Config
======================

.. code-block:: python

  from chat.qa import Robot
  from chat.config import getConfig
  
  robot = Robot(password=getConfig("neo4j", "password"))
  # 返回已有知识库列表
  result = robot.configure(info="")
  # 配置已有知识库权限
  # result = robot.configure(info="在已有知识库列表里选择你想要的名称并以空格分隔")
  print(result)
