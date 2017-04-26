API - 语义工具箱
========================

.. image:: my_figs/semantic.ico 
.. automodule:: chat.semantic

.. autosummary::

   synonym_cut
   get_tag
   sum_cosine
   jaccard_basic
   jaccard
   edit_distance
   similarity
   get_location
   get_musicinfo
   
自定义分词
------------------------
.. autofunction:: synonym_cut

获取语义标签
------------------------
.. autofunction:: get_tag

根据语义分词Cosine相似性矩阵计算语义jaccard模型的各个参数
----------------------------------------------------------------------------------
.. autofunction:: sum_cosine

向量相似度计算-基础jaccard模型
-------------------------------------------
.. autofunction:: jaccard_basic

向量相似度计算-语义jaccard模型
-------------------------------------------
.. autofunction:: jaccard

向量相似度计算-语义编辑距离模型
-------------------------------------------
.. autofunction:: edit_distance

向量相似度计算（模型参数可选）
-------------------------------------------
.. autofunction:: similarity

从句子中获取地名信息
-------------------------------------------
.. autofunction:: get_location

从句子中获取音乐信息
-------------------------------------------
.. autofunction:: get_musicinfo