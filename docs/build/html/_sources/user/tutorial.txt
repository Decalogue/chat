.. _tutorial:

======================
快速开始
======================

对话 QA
======================

* Step 1：在终端中启动数据库(需自定义数据库，其密码设为'train'，可在 chat/conf/self.conf 中修改 [neo4j] 选项 password)

.. code-block:: bash
  
  neo4j start

* Step 2：直接使用 chat 子模块

.. code-block:: python

  from chat.qa import Robot
  from chat.config import getConfig
  
  robot = Robot(password=getConfig("neo4j", "password"))
  answer = robot.search(question="您的自定义问题")
  print(answer)

* Step 2-1：或者先启动语义服务器

.. code-block:: python

  from chat import server
  
  server.start()

* Step 2-2：通过客户端问答

.. code-block:: python

  import json
  from chat.client import match
  
  result = json.loads(match(question="您的自定义问题"))
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
