API - 语义工具箱
========================

.. image:: my_figs/semantic.ico 
.. automodule:: chat.semantic

.. autosummary::

   load_dict
   generate_swords
   check_swords
   synonym_cut
   get_tag
   get_tags
   sim_tag
   max_sim_tag
   sum_cosine
   jaccard_basic
   jaccard
   jaccard2
   edit_distance
   similarity
   similarity2
   get_location
   get_musicinfo

通过 pkl 文件加载原生字典对象
------------------------
.. autofunction:: load_dict

生成敏感词词典
------------------------
.. autofunction:: generate_swords

检测是否包含敏感词
------------------------
.. autofunction:: check_swords

自定义分词（包含标点及语气词过滤）
------------------------
.. autofunction:: segment

自定义分词（可将句子切分为同义词向量标签）
------------------------
.. autofunction:: synonym_cut

获取句子语义标签
------------------------
.. autofunction:: get_tag

获取词对应的语义标签集合
------------------------
.. autofunction:: get_tags

计算两个语义标签的相似度，得分区间为[0, 1]
------------------------
.. autofunction:: sim_tag

计算两个词对应的语义标签集合中标签的最大相似度，得分区间为[0, 1]
------------------------
.. autofunction:: max_sim_tag

根据语义分词Cosine相似性矩阵计算语义jaccard模型的各个参数
----------------------------------------------------------------------------------
.. autofunction:: sum_cosine

向量相似度计算-基础 jaccard 模型
-------------------------------------------
.. autofunction:: jaccard_basic

向量相似度计算-语义 jaccard 模型
-------------------------------------------
.. autofunction:: jaccard

向量相似度计算-语义 jaccard2 模型
-------------------------------------------
.. autofunction:: jaccard2

向量相似度计算-语义编辑距离模型
-------------------------------------------
.. autofunction:: edit_distance

向量相似度计算（模型参数可选）
-------------------------------------------
.. autofunction:: similarity

计算两个句子的相似度，得分区间为[0, 1]
-------------------------------------------
.. autofunction:: similarity2

从句子中获取地名信息
-------------------------------------------
.. autofunction:: get_location

从句子中获取音乐信息
-------------------------------------------
.. autofunction:: get_musicinfo