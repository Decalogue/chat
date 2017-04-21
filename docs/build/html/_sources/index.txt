Chat: 基于自然语言理解与机器学习的聊天机器人。
==========================================================

.. image:: user/my_figs/chat.png
  :scale: 100 %
  :align: center
  :target: https://github.com/decalogue/chat

这就是Chat
---------------

Chat是一个基于自然语言理解与机器学习的语义理解库。
Chat提供丰富的语义分析工具与语义知识图的构建工具，非常适合从0开始迅速搭建自己的聊天机器人，也能够减少工程师在实际开发当中的重复工作。Chat非常易于修改和扩展，所以个性化定制也是非常方便的。如果你有如下需求，欢迎选择Chat：
  
* 想从0开始迅速搭建自己的聊天机器人
* 想了解自然语言处理以及如何构建自己的知识图谱
* 想智能化生活工作，提升效率

Chat适用的Python版本是：Python 3.3-3.5

Chat的设计原则

* 用户友好：用户的使用体验始终是我们考虑的首要和中心内容。Chat遵循减少认知困难的最佳实践：Chat提供一致而简洁的API， 能够极大减少一般应用下用户的工作量，同时，Chat提供清晰和具有实践意义的bug反馈。
* 模块性：完全独立可配置的模块可以用最少的代价自由组合在一起，你可以使用它们来构建自己的模块。
* 易扩展性：添加新模块超级容易，只需要仿照现有的模块编写新的类或函数即可。创建新模块的便利性使得Chat更适合于快速开发。
* 知识图谱：基于图数据库的知识图表达提供了更快的搜索速度与智能。

关于Chat-cn
-------------------

由于作者水平和研究方向所限，因此文档中不可避免会出现各种错误、疏漏和不足之处。如果您在使用过程中有任何意见、建议和疑问，欢迎发送邮件到1044908508@qq.com与我取得联系。

您对文档的任何贡献，包括文档的翻译、查缺补漏、概念解释、发现和修改问题、贡献示例程序等，均会被记录在致谢，十分感谢您对Chat中文文档的贡献！

当前版本与更新
-------------------

如果你发现本文档提供的信息有误，有两种可能：

* 你的Chat版本过低：Chat是一个发展迅速的语义理解库，请保持您的Chat与官方最新的release版本相符
* 我们的中文文档没有及时更新：如果是这种情况，请发邮件给我，我会尽快更新

目前文档的版本号是1.0.3，对应于官方的1.0.3 release 版本, 本次更新的主要内容是：

* 文档全面升级，绝大多数API均得到更新
* 补充了原文档中缺失，但源代码中确实可用的类和函数
* 重新整理了文档风格和栏目，使得文档更容易阅读

.. note::
  我们建议你在 `Github <https://github.com/decalogue/chat>`_ 上star和watch `官方项目 <https://github.com/decalogue/chat>`_ ，这样当官方有更新时，你会立即知道。
  
  如果你阅读在线中文文档时有什么问题，你可以在github上下载这个项目，
  然后去 ``/docs/build/html/index.html`` 阅读离线中文文档。
  或者在 `Read the docs <http://chat-cn.readthedocs.io/zh_CN/latest/>`_ 中阅读官方原文档。

用户指南
---------------

.. toctree::
   :maxdepth: 2

   user/installation
   user/tutorial
   user/custom
   user/development
   user/architecture
   user/tss
   user/thanks

API目录
----------

如果你正在寻找某个特殊的函数，类或者方法，这一列文档就是为你准备的。

.. toctree::
  :maxdepth: 2
  
  modules/server
  modules/client
  modules/qa
  modules/semantic
  modules/database
  modules/mytools
  modules/upload
  modules/download


索引与附录
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _GitHub: https://github.com/decalogue/chat

