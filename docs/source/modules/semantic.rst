API - 语义工具箱
========================

.. image:: my_figs/semantic.ico
  :scale: 50 %

.. automodule:: chat.semantic

.. autosummary::

   semantic.load_dict
   semantic.generate_swords
   semantic.check_swords
   semantic.synonym_cut
   semantic.get_tag
   semantic.get_tags
   semantic.sim_tag
   semantic.max_sim_tag
   semantic.sum_cosine
   semantic.jaccard_basic
   semantic.jaccard
   semantic.jaccard2
   semantic.edit_distance
   semantic.similarity
   semantic.similarity2
   semantic.get_location
   semantic.get_musicinfo

通过 pkl 文件加载原生字典对象
------------------------
.. autofunction:: semantic.load_dict

生成敏感词词典
------------------------
.. autofunction:: semantic.generate_swords

检测是否包含敏感词
------------------------
.. autofunction:: semantic.check_swords

自定义分词（包含标点及语气词过滤）
------------------------
.. autofunction:: segment

自定义分词（可将句子切分为同义词向量标签）
------------------------
.. autofunction:: semantic.synonym_cut

获取句子语义标签
------------------------
.. autofunction:: semantic.get_tag

获取词对应的语义标签集合
------------------------
.. autofunction:: semantic.get_tags

计算两个语义标签的相似度，得分区间为[0, 1]
------------------------
.. autofunction:: semantic.sim_tag

计算两个词对应的语义标签集合中标签的最大相似度，得分区间为[0, 1]
------------------------
.. autofunction:: semantic.max_sim_tag

根据语义分词Cosine相似性矩阵计算语义jaccard模型的各个参数
----------------------------------------------------------------------------------
.. autofunction:: semantic.sum_cosine

向量相似度计算-基础 jaccard 模型
-------------------------------------------
.. autofunction:: semantic.jaccard_basic

向量相似度计算-语义 jaccard 模型
-------------------------------------------
.. autofunction:: semantic.jaccard

向量相似度计算-语义 jaccard2 模型
-------------------------------------------
.. autofunction:: semantic.jaccard2

向量相似度计算-语义编辑距离模型
-------------------------------------------
.. autofunction:: semantic.edit_distance

向量相似度计算（模型参数可选）
-------------------------------------------
.. autofunction:: semantic.similarity

计算两个句子的相似度，得分区间为[0, 1]
-------------------------------------------
.. autofunction:: semantic.similarity2

从句子中获取地名信息
-------------------------------------------
.. autofunction:: semantic.get_location

从句子中获取音乐信息
-------------------------------------------
.. autofunction:: semantic.get_musicinfo
