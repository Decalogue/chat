.. _development:

=====================
开发 Development
=====================

Chat始于一个本地语义理解项目，目前由数位 `GitHub`_ 的贡献者负责维护和进行改进。

作为一个为研究员和工程师开发的开源项目，我们诚挚地欢迎您为对项目提供帮助。
每个微小的支持都会帮助我们并且会被记录下来。

理念
====================

Chat的想法源于组合语义标签的高区分度和图数据库的灵活高速查询以及向量语义相似度算法的高精度匹配。
它依照下列设计目标所开发：

* **简洁**：易于使用，易于扩展与修改以便于研究和工程中使用。
* **快速**：自定义语义标签词典：切词过程直接切分为语义向量；图数据库高速查询复杂关联数据；高速语义矩阵相似度计算。简洁但不牺牲性能。
* **兼容**：chat的每个功能模块都很方便替换为功能相同的其它模块。
* **透明**：所有模块均使用纯Python来实现，没有一些实现原理及功能的隐藏。

如何参与我们
"""""""""""""

如果您在自然语言理解和问答系统发布了新的算法或者有建设性的想法，
欢迎您分享给Chat

* 说明它是怎么工作的，如果可以话请给出学术论文的链接。
* 尽可能地缩减其范围，以以致于便于实现


报告BUG
"""""""""""""""""""

请您在 `GitHub`_ 上报告BUG。
如果您打算报告BUG，请包含以下内容：

* 您的项目依赖库的版本号
* 重现BUG的步骤，最好能减少到数个python 命令
* 您获得的结果和您期望的结果。

如果您不确定遇到的行为是否是BUG，
或者你不确定错误是否与Chat有关，
请您先在 `our mailing list`_ 查看下。

修复BUG
"""""""""""""

通过GitHub的问题栏(issues)来查看BUG报告。
任何被标记为BUG的项对所有想要修复它的人来说都是开放的。
如果您发现了Chat的一个你可以自己修复的BUG，
您可以用任何方法来实现修复并且无需立即报告这个BUG。

编写文档
""""""""""""""

无论什么时候您发现有些文档没有解释清楚，存在误导，敷衍带过或者根本就是错的。请及时更新它！*Edit on GitHub* 的链接就在每一篇文档的右上角并且API引用列表中的每篇文档的*[source]*的链接可以帮助您快速地定位任何文字的根源。

如何参与我们
====================

在GitHub上编辑
"""""""""""""""""""

正如刚刚文档中修复BUG所说的简单方法，
点击文档右上角的*Edit on GitHub*链接或者API引用列表中的对象的*[source]*链接来打开GitHub中的源文件，
然后在你的浏览器中点击*Edit this file*链接并发送拉请求(Pull Request).
你只需要一个免费的GitHub账户就可以做到了。

对于任何较大幅度的修改，请遵循以下步骤来更新Chat开发。

文档
""""""""""""""

文档由 `Sphinx <http://sphinx-doc.org/latest/index.html>`_ 生成。
如果要本地编辑它，运行下列命令：
.. code:: bash

    cd docs
    make html

如果您想要重新生成整个文档，运行下列命令：

.. code:: bash

    cd docs
    make clean
    make html

然后，打开 ``docs/build/index.html`` 来查看会出现在 `Read the docs <http://chat-cn.readthedocs.io/zh_CN/latest/>`_ 文档。如果您更改了很多内容，并且似乎出现了许多误导性的错误信息或警告，运行``make clean html``来让Sphinx重新生成所有文件。

编写英文文档文字时，请尽可能地按照现有文档的文字习惯，
来保证整个库文字的一致性。所使用的语法及约定的相关信息，请参考以下文档：

* `reStructuredText Primer <http://sphinx-doc.org/rest.html>`_
* `Sphinx reST markup constructs <http://sphinx-doc.org/markup/index.html>`_
* `A Guide to NumPy/SciPy Documentation <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`_

测试
"""""""""

* 每当您更改任何代码的时候，您应该运行测试脚本来测试它是否能优化现有属性。
* 您修改的每个BUG说明一个缺少的测试案例，所以每个修复BUG的方案应该配置一个您没修复前的测试案例。

发送拉请求
"""""""""""""""""

当您对您添加的内容感到满意并且测试通过，文档规范，简明，不存在任何注释错误。
您可以将您的更改提交到一个新的分支(branch)，并且将这个分支与您的副本(fork)合并，
然后通过GitHub的网站发送一个拉请求(pull request)

所有的这些步骤在GitHub上有相当不错的说明：
https://guides.github.com/introduction/flow/

当您提交拉请求时，请附带一个更改内容的说明，以帮助我们能更好的检阅它。
如果它是一个正在开放的问题(issue)，比如：issue#123，请在您的描述中添加
*Fixes#123*,*Resolves#123*或者*Closes#123*，这样当您的拉请求被接纳之后
GitHub会关闭那个问题。


.. _GitHUb: http://github.com/decalogue/chat
.. _our mailing list: 1044908508@qq.com
