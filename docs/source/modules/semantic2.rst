API - 语义工具箱2
========================

.. image:: my_figs/semantic2.ico 
.. automodule:: chat.semantic2

.. autosummary::

   process_part
   build_tagtree
   build_tagcount_1
   build_tagcount_2
   build_tagcount_3
   build_tagcount_4
   load_dict

按行读取文件进行自定义处理，直到遇到空行或者到达文件末尾为止
------------------------
.. autofunction:: process_part

构建语义标签树
------------------------
.. autofunction:: build_tagtree

构建第1级编码语义标签树
------------------------
.. autofunction:: build_tagcount_1

构建前2级编码语义标签树
------------------------
.. autofunction:: build_tagcount_2

构建前3级编码语义标签树
------------------------
.. autofunction:: build_tagcount_3

构建前4级编码语义标签树
------------------------
.. autofunction:: build_tagcount_4

通过 pkl 文件加载原生字典对象
------------------------
.. autofunction:: load_dict
