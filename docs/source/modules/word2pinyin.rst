API - 拼音语义算法
========================

.. image:: my_figs/word2pinyin.ico 
.. automodule:: chat.word2pinyin

.. autosummary::

   sum_cosine
   match_pinyin
   jaccard_pinyin
   pinyin_cut
   similarity_pinyin
   
根据语义分词Cosine相似性矩阵计算语义 jaccard 模型的各个参数
------------------------
.. autofunction:: sum_cosine

计算两个拼音的相似度得分
------------------------
.. autofunction:: match_pinyin

计算两个拼音向量的语义 jaccard 相似度得分
------------------------
.. autofunction:: jaccard_pinyin

将句子切分为拼音向量
------------------------
.. autofunction:: pinyin_cut

基于拼音向量的语义 jaccard 句子相似度得分
------------------------
.. autofunction:: similarity_pinyin