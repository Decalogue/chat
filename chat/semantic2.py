# -*- coding: utf-8 -*-
import os
import math
import pickle
import jieba
import numpy as np
from string import punctuation

# 初始化语义标签树
tagtree = {}
tagcount_1 = {}
tagcount_2 = {}
tagcount_3 = {}
tagcount_4 = {}

# 语义标签树 pkl 文件绝对路径
thispath = os.path.split(os.path.realpath(__file__))[0]
sourcepath = thispath + './dict/synonym.txt'
pkl_tagtree = thispath + './dict/tagtree.pkl'
pkl_tagcount_1 = thispath + './dict/tagcount_1.pkl'
pkl_tagcount_2 = thispath + './dict/tagcount_2.pkl'
pkl_tagcount_3 = thispath + './dict/tagcount_3.pkl'
pkl_tagcount_4 = thispath + './dict/tagcount_4.pkl'

# 中英文标点组合
punctuation_zh = " 、，。°？！：；“”’‘～…【】（）《》｛｝×―－·→℃"
punctuation_all = set(punctuation) | set(punctuation_zh)
# 句尾语气词
tone_words = "的了呢吧吗啊啦呀"
            
def process_part(path, func=None):
    """按行读取文件进行自定义处理，直到遇到空行或者到达文件末尾为止。
    """
    with open(path, 'r', encoding='UTF-8') as fp:
        for line in iter(fp.readline, ''):
            func(line)

def build_tagtree(line):
    """构建语义标签树
    """
    if line.rstrip(): # 排除空字符串或者换行情况
        content = line.split()
        word = content[0]
        tag = content[2]
        tagtree.setdefault(word, []).append(tag)

def build_tagcount_1(line):
    """构建第1级编码语义标签树
    """
    if line:
        content = line.split()
        tag = content[2][0]
        if tag not in tagcount_1:
            tagcount_1[tag] = 0
        else:
            tagcount_1[tag] += 1

def build_tagcount_2(line):
    """构建前2级编码语义标签树
    """
    if line:
        content = line.split()
        tag = content[2][:2]
        if tag not in tagcount_2:
            tagcount_2[tag] = 0
        else:
            tagcount_2[tag] += 1

def build_tagcount_3(line):
    """构建前3级编码语义标签树
    """
    if line:
        content = line.split()
        tag = content[2][:4]
        if tag not in tagcount_3:
            tagcount_3[tag] = 0
        else:
            tagcount_3[tag] += 1

def build_tagcount_4(line):
    """构建前4级编码语义标签树
    """
    if line:
        content = line.split()
        tag = content[2][:5]
        if tag not in tagcount_4:
            tagcount_4[tag] = 0
        else:
            tagcount_4[tag] += 1

def load_dict(path=''):
    """通过 pkl 文件加载原生字典对象
    """
    if os.path.isfile(path):
        with open(path, 'rb') as fp:
            return pickle.load(fp)
    else:
        return {}        

# 加载语义标签树
tagtree = load_dict(path=pkl_tagtree)
if not tagtree:
    print("Load tagtree failed")
    process_part(sourcepath, func=build_tagtree)
    with open(pkl_tagtree, 'wb') as fp:
        pickle.dump(tagtree, fp)
        
tagcount_1 = load_dict(path=pkl_tagcount_1)
if not tagcount_1:
    print("Load tagcount_1 failed")
    process_part(sourcepath, func=build_tagcount_1)
    with open(pkl_tagcount_1, 'wb') as fp:
        pickle.dump(tagcount_1, fp)
        
tagcount_2 = load_dict(path=pkl_tagcount_2)
if not tagcount_2:
    print("Load tagcount_2 failed")
    process_part(sourcepath, func=build_tagcount_2)
    with open(pkl_tagcount_2, 'wb') as fp:
        pickle.dump(tagcount_2, fp)
        
tagcount_3 = load_dict(path=pkl_tagcount_3)
if not tagcount_3:
    print("Load tagcount_3 failed")
    process_part(sourcepath, func=build_tagcount_3)
    with open(pkl_tagcount_3, 'wb') as fp:
        pickle.dump(tagcount_3, fp)
        
tagcount_4 = load_dict(path=pkl_tagcount_4)
if not tagcount_4:
    print("Load tagcount_4 failed")
    process_part(sourcepath, func=build_tagcount_4)
    with open(pkl_tagcount_4, 'wb') as fp:
        pickle.dump(tagcount_4, fp)

def get_tags(word):
    """获取词对应的语义标签集合
    """
    return tagtree.setdefault(word, [])
    
def sim_tag(tag1, tag2):
    """计算两个语义标签的相似度，得分区间为[0, 1]。
    """
    score = 0.1
    n = 0 # n 是分支层的节点总数
    d = 0 # d 是两个分支间的距离
    s1 = 0.65
    s2 = 0.8
    s3 = 0.9
    s4 = 0.96
    if tag1 == tag2:               # 语义标签相等
        if tag1[7] == '=':          # 在第五层相等
            score = 0.95
        else:
            score = 0.5
    elif tag1[:5] == tag2[:5]:      # 在第4层相等 int
        n = tagcount_4.setdefault(tag1[:5], 0)
        d = abs(int(tag1[5:7]) - int(tag2[5:7]))
        return math.cos(n * math.pi / 180) * ((n - d + 1) / n) * s4
    elif tag1[:4] == tag2[:4]:      # 在第3层相等 ord
        n = tagcount_3.setdefault(tag1[:4], 0)
        d = abs(ord(tag1[4:5]) - ord(tag2[4:5]))
        return math.cos(n * math.pi / 180) * ((n - d + 1) / n) * s3
    elif tag1[:2] == tag2[:2]:      # 在第2层相等 int
        n = tagcount_2.setdefault(tag1[:2], 0)
        d = abs(int(tag1[2:4]) - int(tag2[2:4]))
        return math.cos(n * math.pi / 180) * ((n - d + 1) / n) * s2
    elif tag1[:1] == tag2[:1]:      # 在第1层相等 ord
        n = tagcount_1.setdefault(tag1[:1], 0)
        d = abs(ord(tag1[1:2]) - ord(tag2[1:2]))
        return math.cos(n * math.pi / 180) * ((n - d + 1) / n) * s1
    return score

def max_sim_tag(word1, word2):
    """计算两个词对应的语义标签集合中标签的最大相似度，得分区间为[0, 1]。
    """
    if word1 == word2:
        return 1.0
    max_score = 0
    score = 0
    tags1 = get_tags(word1)
    tags2 = get_tags(word2)
    if not tags1 or not tags2: # 至少有一个语义标签集合为空
        return 0.1
    for t1 in tags1:
        for t2 in tags2:
            score = sim_tag(t1, t2)
            if score > max_score:
                max_score = score
            if max_score == 1:
                return max_score
    return max_score

def sum_cosine(matrix, threshold):
    """Calculate the parameters of the semantic Jaccard model based on the
    Cosine similarity matrix of semantic word segmentation.
    根据语义分词Cosine相似性矩阵计算语义jaccard模型的各个参数。

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
    zero_row = np.zeros([1, col])
    zero_col = np.zeros([row, 1])
    max_score = matrix.max()
    while max_score > threshold:
        total += max_score
        count += 1
        pos = np.where(matrix == max_score)
        i = pos[0][0]
        j = pos[1][0]
        matrix[i, :] = zero_row
        matrix[:, j] = zero_col
        max_score = matrix.max()
    num = (row - count) if row > col else (col - count)
    return dict(total=total, num_not_match=num, total_dif=max_score)
    
def jaccard(sv1, sv2, threshold=0.8):
    """Similarity score between two vectors with jaccard.
    两个向量的语义jaccard相似度得分。

    According to the semantic jaccard model to calculate the similarity.
    The similarity score interval for each two sentences was [0, 1].
    根据语义jaccard模型来计算相似度。每两个向量的相似度得分区间为[0, 1]。
    
    分词：自定义词典
    单词相似度：从语义标签树中获取两个单词对应的语义标签集合，计算它们在分级编码
    语义标签树中的距离
    算法：基于词向量相似度矩阵 + 向量余弦
    
    实现：通过计算语义标签（使用哈工大同义词词林）相似度矩阵，比较两词相似度。
    1.阈值：0.8，每两个语义标签的相似度区间：[0,1]，若无标签则计算原词相似度得分。
    2.计算两个标签相似度得分：词林提供三层编码：第一级大类用大写英文字母表示，
    第二级中类用小写字母表示，第三级小类用二位十进制整数表示，第四级词群用大写
    英文字母表示，第五级原子词群用二位十进制整数表示。第八位的标记有三种，分别
    是“=“、”#“、”@“，=代表相等、同义，#代表不等、同类，@代表自我封闭、独立，
    它在词典中既没有同义词，也没有相关词。
    """
    sv_matrix = []
    sv_rows = []
    n = 0 # n是分支层的节点总数
    k = 0 # k是两个分支间的距离
    a = 0.65
    b = 0.8
    c = 0.9
    d = 0.96
    for word1 in sv1:
        for word2 in sv2:
            score = max_sim_tag(word1, word2)
            sv_rows.append(score)
        sv_matrix.append(sv_rows)
        sv_rows = []
    matrix = np.mat(sv_matrix)
    result = sum_cosine(matrix, threshold)
    total = result["total"]
    total_dif = result["total_dif"]
    num = result["num_not_match"]
    sim = total/(total + num*(1-total_dif))
    return sim

def segment(sentence):
    """过滤分词。
    """
    # 句尾标点符号过滤
    s = sentence.rstrip(''.join(punctuation_all))
    # 句尾语气词过滤
    s = s.rstrip(tone_words)
    # 句中标点符号过滤
    sv = [word for word in jieba.cut(s) if word not in punctuation_all]
    return sv
    
def similarity(s1, s2):
    """Similarity score between two sentences.
    计算两个句子的相似度，得分区间为[0, 1]。
    """
    assert s1 != '', "sentence can not be empty"
    assert s2 != '', "sentence can not be empty"
    if s1 == s2:
        return 1.0
    return jaccard(segment(s1), segment(s2))
