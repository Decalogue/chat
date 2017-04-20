.. _tutorial:

======================
快速开始
======================

对话
======================

.. code-block:: python

  from chat.qa import Robot
  
  robot = Robot()
  answer = robot.search(question="你好", userid="userid")
  print(answer)
  
配置
======================

.. code-block:: python

  from chat.qa import Robot
  
  robot = Robot()
  answer = robot.config(info="", userid="userid")
  print(answer)
