# Chat

`Chat robot based on natural language understanding and machine learning.`

`基于自然语言理解与机器学习的聊天机器人`

[![Documentation Status](https://readthedocs.org/projects/chat-cn/badge/?version=latest)](http://chat-cn.readthedocs.io/zh_CN/latest/?badge=latest)

## 这就是Chat

* Chat是一个基于自然语言理解与机器学习的语义理解库。
* Chat提供丰富的语义分析工具与语义知识图的构建工具，非常适合从0开始迅速搭建自己的聊天机器人，也能够减少工程师在实际开发当中的重复工作。
* Chat非常易于修改和扩展，所以个性化定制也是非常方便的。如果您有如下需求，欢迎选择Chat：
  
  * 想从0开始迅速搭建自己的聊天机器人
  * 想了解自然语言处理以及如何构建自己的知识图谱
  * 想智能化生活工作，提升效率

> Chat适用的Python版本是：**Python 3.3-3.5**

## Installation 安装

    pip install chat
    
## Tutorial 快速开始

    from chat.qa import Robot
  
    robot = Robot()
    answer = robot.search(question="您好", userid="userid")
    print(answer)

## Chat的设计原则

* 用户友好：用户的使用体验始终是我们考虑的首要和中心内容。Chat遵循减少认知困难的最佳实践：Chat提供一致而简洁的API， 能够极大减少一般应用下用户的工作量，同时，Chat提供清晰和具有实践意义的bug反馈。
* 模块性`：完全独立可配置的模块可以用最少的代价自由组合在一起，您可以使用它们来构建自己的模块。
* 易扩展性：添加新模块超级容易，只需要仿照现有的模块编写新的类或函数即可。创建新模块的便利性使得Chat更适合于快速开发。
* 知识图谱：基于图数据库的知识图表达提供了更快的搜索速度与智能。

> 如果您阅读在线中文文档时有什么问题，您可以在github上下载这个项目，然后去 ***/docs/build/html/index.html*** 阅读离线中文文档。或者在[Read the docs](http://chat-cn.readthedocs.io/zh_CN/latest/)中阅读官方原文档。

`Copyright © 2017 Rain. All Rights Reserved.`

[樱落清璃-Decalogue的CSDN博客](https://www.decalogue.cn)
