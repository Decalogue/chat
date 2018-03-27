#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PEP 8 check with Pylint
"""Word to pinyin.
"""
from numpy import mat, zeros, where
from pypinyin import pinyin, lazy_pinyin
# from .mytools import time_me

def sum_cosine(matrix, threshold):
    """Calculate the parameters of the semantic Jaccard model based on the
    Cosine similarity matrix of semantic word segmentation.
    根据语义分词Cosine相似性矩阵计算语义 jaccard 模型的各个参数。

    Args:
        matrix: Semantic Cosine similarity matrix. 语义分词Cosine相似性矩阵。
        threshold: Threshold for semantic matching. 达到语义匹配标准的阈值。

    Returns:
        total: The semantic intersection of two sentence language fragments.
            两个句子语言片段组成集合的语义交集。
        num_not_match: The total number of fragments or the maximum value of two sets
		    that do not meet the semantic matching criteria controlled by the threshold.
		    两个集合中没有达到语义匹配标准（由阈值threshold控制）的总片段个数或者两者中取最大值。
        total_dif: The degree of semantic difference between two sets.
            两个集合的语义差异程度。
    """
    total = 0
    count = 0
    row = matrix.shape[0]
    col = matrix.shape[1]
    zero_row = zeros([1, col])
    zero_col = zeros([row, 1])
    max_score = matrix.max()
    while max_score > threshold:
        total += max_score
        count += 1
        pos = where(matrix == max_score)
        i = pos[0][0]
        j = pos[1][0]
        matrix[i, :] = zero_row
        matrix[:, j] = zero_col
        max_score = matrix.max()
    num = (row - count) if row > col else (col - count)
    return dict(total=total, num_not_match=num, total_dif=max_score)

def match_pinyin(pinyin1, pinyin2):
    """Similarity score between two pinyin.
    计算两个拼音的相似度得分。
    """
    assert pinyin1 != "", "pinyin1 can not be empty"
    assert pinyin2 != "", "pinyin2 can not be empty"
    pv_match = 0
    if len(pinyin1) < len(pinyin2):
        len_short = len(pinyin1)
        len_long = len(pinyin2)
        pv_long = pinyin2
        pv_short = pinyin1
    else:
        len_short = len(pinyin2)
        len_long = len(pinyin1)
        pv_long = pinyin1
        pv_short = pinyin2
    for i in range(0, len_short):
        if pv_short[i] == pv_long[i]:
            pv_match += 1
    score = pv_match/len_long
    return score
    
def jaccard_pinyin(pv1, pv2, threshold=0.7):
    """Similarity score between two pinyin vectors with jaccard.
    计算两个拼音向量的语义 jaccard 相似度得分。

    According to the semantic jaccard model to calculate the similarity.
    The similarity score interval for each two pinyin sentences was [0, 1].
    根据语义jaccard模型来计算相似度。每两个拼音向量的相似度得分区间为为[0, 1]。
    """
    sv_matrix = []
    sv_rows = []
    for pinyin1 in pv1:
        for pinyin2 in pv2:
            score = match_pinyin(pinyin1, pinyin2)
            sv_rows.append(score)
        sv_matrix.append(sv_rows)
        sv_rows = []
    matrix = mat(sv_matrix)
    result = sum_cosine(matrix, threshold)
    total = result["total"]
    total_dif = result["total_dif"]
    num = result["num_not_match"]
    sim = total/(total + num*(1-total_dif))
    return sim

def pinyin_cut(sentence, pattern=None):
    """Cut the sentence into phonetic vectors.
    将句子切分为拼音向量。
    """
    return lazy_pinyin(sentence)

# @time_me()    
def similarity_pinyin(sentence1, sentence2):
    """Similarity score between two based on pinyin vectors with jaccard.
    基于拼音向量的语义 jaccard 句子相似度得分。
    """
    pv1 = pinyin_cut(sentence1)
    pv2 = pinyin_cut(sentence2)
    return jaccard_pinyin(pv1, pv2)

if __name__ == '__main__':
    print(similarity_pinyin("我想办理粤通卡", "办理悦通卡"))
