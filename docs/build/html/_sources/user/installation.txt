.. _installation:

======================
安装 Installation
======================

一、图形数据库
======================

1.Neo4j简介
--------------------------

Neo4j是一个高性能的,NOSQL图形数据库，它将结构化数据存储在网络上而不是表中。Neo4j也可以被看作是一个高性能的图引擎，该引擎具有成熟数据库的所有特性。程序员工作在一个面向对象的、灵活的网络结构下而不是严格、静态的表中——但是他们可以享受到具备完全的事务特性、企业级的数据库的所有好处。

2.图形数据结构
--------------------------

在一个图中包含两种基本的数据类型：Nodes（节点） 和 Relationships（关系）。Nodes 和 Relationships 包含key/value形式的属性。Nodes通过Relationships所定义的关系相连起来，形成关系型网络结构。

.. image:: my_figs/neo4j.png

3.Neo4j安装
--------------------------

Neo4j可以被安装成一个独立运行的服务端程序，客户端程序通过REST API进行访问。也可以嵌入式安装，即安装为编程语言的第三方类库，目前只支持Java和Python语言。因Neo4j是用Java语言开发的，所以确保将要安装的机器上已安装了jre或者jdk。

此种安装方式简单，各平台安装过程基本一样

* 1.从 `Neo4j官网 <https://neo4j.org/download>`_ 上下载最新的版本，根据安装的平台选择适当的版本。
* 2.解压安装包，解压后运行终端，进入解压后文件夹中的bin文件夹。
* 3.在终端中运行命令完成安装。
  
.. code-block:: bash
  
  neo4j install-service
    
* 4.在终端中运行命令开启服务。
  
.. code-block:: bash
  
  neo4j start
    
* 5.通过stop命令可以关闭服务，status命令查看运行状态。

二、Python3
======================

1.Anaconda
-------------------

从 `Anaconda官网 <https://www.continuum.io/downloads>`_ 上下载3.5版本，根据安装的平台选择适当的版本。

2.Python依赖包
-------------------

从requirements.txt安装，由于安装chat时会自动安装依赖，所以这一步也可省略。

* api
* jieba
* numpy
* py2neo
* requests
* xlrd
* xlwt

.. code-block:: bash
  
  pip install -r requirements.txt

三、Chat
======================

.. code-block:: bash
  
  pip install chat


