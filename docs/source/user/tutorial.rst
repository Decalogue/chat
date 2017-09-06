.. _tutorial:

======================
快速开始
======================

对话 QA
======================

* Step 1：在终端中启动数据库

.. code-block:: bash
  
  neo4j start

* Step 2：直接使用 chat 子模块

.. code-block:: python

  from chat.qa import Robot
  
  robot = Robot()
  # 此处 userid 是你的机器人配置信息中的 userid
  answer = robot.search(question="你好", userid="userid")
  print(answer)

* Step 2-1：或者先启动语义服务器

.. code-block:: python

  from chat import server
  
  server.start()

* Step 2-2：通过客户端问答

.. code-block:: python

  import json
  from chat.client import match
  
  result = json.loads(match(question="你的问题", userid="userid"))
  answer = result['content']
  print(answer)
  
配置 Config
======================

.. code-block:: python

  from chat.qa import Robot
  
  robot = Robot()
  # 返回已有知识库列表
  answer = robot.config(info="", userid="userid")
  # 配置已有知识库权限
  # answer = robot.config(info="在已有知识库列表里选择你想要的名称并以空格分隔", userid="userid")
  print(answer)
