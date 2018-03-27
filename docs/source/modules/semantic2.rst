API - 语义工具箱2
========================

.. image:: my_figs/semantic.ico
  :scale: 50 %

.. automodule:: chat.semantic2

.. autosummary::

   semantic2.process_part
   semantic2.build_tagtree
   semantic2.build_tagcount_1
   semantic2.build_tagcount_2
   semantic2.build_tagcount_3
   semantic2.build_tagcount_4
   semantic2.load_dict

按行读取文件进行自定义处理，直到遇到空行或者到达文件末尾为止
------------------------
.. autofunction:: semantic2.process_part

构建语义标签树
------------------------
.. autofunction:: semantic2.build_tagtree

构建第1级编码语义标签树
------------------------
.. autofunction:: semantic2.build_tagcount_1

构建前2级编码语义标签树
------------------------
.. autofunction:: semantic2.build_tagcount_2

构建前3级编码语义标签树
------------------------
.. autofunction:: semantic2.build_tagcount_3

构建前4级编码语义标签树
------------------------
.. autofunction:: semantic2.build_tagcount_4

通过 pkl 文件加载原生字典对象
------------------------
.. autofunction:: semantic2.load_dict
