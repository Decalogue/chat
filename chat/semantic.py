# -*- coding: utf-8 -*-
"""A collection of semantic tools. 语义工具集合。

Use 'jieba' as Chinese word segmentation tool. The 'set_dictionary' and
'load_userdict' must before import 'jieba.posseg' and 'jieba.analyse'.
采用'jieba'作为中文分词工具，使用自定义分词词典。

Available functions:
- All classes and functions: 所有类和函数
"""
import os
import codecs
import math
import pickle
import numpy as np
import jieba
thispath = os.path.split(os.path.realpath(__file__))[0]
jieba.set_dictionary(thispath + "/dict/synonymdict.txt")
jieba.load_userdict(thispath + "/dict/userdict.txt")
import jieba.posseg as posseg
import jieba.analyse as analyse
from string import punctuation

# 语义标签树 pkl 文件绝对路径
thispath = os.path.split(os.path.realpath(__file__))[0]
pkl_tagtree = thispath + './dict/tagtree.pkl'
pkl_tagcount_1 = thispath + './dict/tagcount_1.pkl'
pkl_tagcount_2 = thispath + './dict/tagcount_2.pkl'
pkl_tagcount_3 = thispath + './dict/tagcount_3.pkl'
pkl_tagcount_4 = thispath + './dict/tagcount_4.pkl'

def load_dict(path=''):
    """通过 pkl 文件加载原生字典对象
    """
    if os.path.isfile(path):
        with open(path, 'rb') as fp:
            return pickle.load(fp)
    else:
        return {} 

tagtree = load_dict(path=pkl_tagtree)
tagcount_1 = load_dict(path=pkl_tagcount_1)
tagcount_2 = load_dict(path=pkl_tagcount_2)
tagcount_3 = load_dict(path=pkl_tagcount_3)
tagcount_4 = load_dict(path=pkl_tagcount_4)

# The 'punctuation_all' is the combination set of Chinese and English punctuation.
punctuation_zh = " 、，。°？！：；“”’‘～…【】（）《》｛｝×―－·→℃"
punctuation_all = set(punctuation) | set(punctuation_zh)
# 句尾语气词 TODO：考虑语气词单独成句的情况
tone_words = "的了呢吧吗啊啦呀"
# 敏感词库 Modified in 2017-5-25
try:
    with codecs.open(thispath + "\\dict\\swords.txt", "r", "UTF-8") as file:
        sensitive_words = set(file.read().split())
except:
    sensitive_words = []

def generate_swords():
    with codecs.open(thispath + "\\dict\\sensitive_words.txt", "r", "UTF-8") as file:
        with codecs.open(thispath + "\\dict\\swords.txt", "w", "UTF-8") as newfile:
            sensitive_words = sorted(list(set(file.read().split())))
            newfile.write("\n".join(sensitive_words))

def check_swords(sentence):
    """检测是否包含敏感词
    """
    for word in sensitive_words:
        if word in sentence:
            return True
    return False
    # words = synonym_cut(sentence, pattern="w")
    # swords = set(sensitive_words).intersection(words)
    # return bool(swords)

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

def synonym_cut(sentence, pattern="wf"):
    """Cut the sentence into a synonym vector tag.
    将句子切分为同义词向量标签。

    If a word in this sentence was not found in the synonym dictionary,
    it will be marked with default value of the word segmentation tool.
    如果同义词词典中没有则标注为切词工具默认的词性。

    Args:
        pattern: 'w'-分词, 'k'-唯一关键词，'t'-关键词列表, 'wf'-分词标签, 'tf-关键词标签'。
    """
    # Modify: 添加完整的句尾标点符号过滤 2018-1-26 Contributor: zheyang0715(https://github.com/zheyang0715)
    sentence = sentence.rstrip(''.join(punctuation_all))
    # 句尾语气词过滤
    sentence = sentence.rstrip(tone_words)
    synonym_vector = []
    if pattern == "w":
        synonym_vector = [item for item in jieba.cut(sentence) if item not in punctuation_all]
    elif pattern == "k":
        synonym_vector = analyse.extract_tags(sentence, topK=1)
    elif pattern == "t":
        synonym_vector = analyse.extract_tags(sentence, topK=10)
    elif pattern == "wf":
        result = posseg.cut(sentence)
        # synonym_vector = [(item.word, item.flag) for item in result \
        # if item.word not in punctuation_all]
        # Modify in 2017.4.27 
        for item in result:
            if item.word not in punctuation_all:
                if len(item.flag) < 4:
                    item.flag = list(posseg.cut(item.word))[0].flag
                synonym_vector.append((item.word, item.flag))
    elif pattern == "tf":
        result = posseg.cut(sentence)
        tags = analyse.extract_tags(sentence, topK=10)
        for item in result:
            if item.word in tags:
                synonym_vector.append((item.word, item.flag))
    return synonym_vector

def get_tag(sentence, config):
    """Get semantic tag of sentence. 获取句子语义标签。
    """
    iquestion = sentence.format(**config)
    try:
        keywords = analyse.extract_tags(iquestion, topK=1)
        keyword = keywords[0]
    except IndexError:
        keyword = iquestion
    tags = synonym_cut(keyword, 'wf') # tuple list
    if tags:
        tag = tags[0][1]
        if not tag:
            tag = keyword
    else:
        tag = keyword
    return tag

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

def jaccard2(sv1, sv2, threshold=0.8):
    """Similarity score between two vectors with jaccard.
    两个向量的语义jaccard相似度得分。

    According to the semantic jaccard model to calculate the similarity.
    The similarity score interval for each two sentences was [0, 1].
    根据语义jaccard模型来计算相似度。每两个向量的相似度得分区间为[0, 1]。
    
    分词：自定义词典
    单词相似度：从语义标签树中获取两个单词对应的语义标签集合，计算它们在分级编码
    语义标签树中的距离
    算法：基于词向量相似度矩阵 + 向量余弦
    
    实现：通过计算语义标签相似度矩阵，比较两词相似度。
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

def jaccard_basic(synonym_vector1, synonym_vector2):
    """Similarity score between two vectors with basic jaccard.
    两个向量的基础jaccard相似度得分。

    According to the bassic jaccard model to calculate the similarity.
    The similarity score interval for each two sentences was [0, 1].
    根据基础jaccard模型来计算相似度。每两个向量的相似度得分区间为为[0, 1]。
    """
    count_intersection = list(set(synonym_vector1).intersection(set(synonym_vector2)))
    count_union = list(set(synonym_vector1).union(set(synonym_vector2)))
    sim = len(count_intersection)/len(count_union)
    return sim

def jaccard(synonym_vector1, synonym_vector2, threshold=0.8):
    """Similarity score between two vectors with jaccard.
    两个向量的语义jaccard相似度得分。

    According to the semantic jaccard model to calculate the similarity.
    The similarity score interval for each two sentences was [0, 1].
    根据语义jaccard模型来计算相似度。每两个向量的相似度得分区间为为[0, 1]。
    
    分词：语义标签词典 + 自定义词典
    单词相似度：基于标签字母前n位相同情况
    算法：基于词向量相似度矩阵 + 向量余弦
    
    实现：通过计算语义标签相似度矩阵，比较两词相似度。
    1.阈值：0.8，每两个语义标签的相似度区间：[0,1]，若无标签则计算原词相似度得分。
    2.计算两个标签相似度得分：根据标签字母前n位相同情况判断得分。
    """
    sv_matrix = []
    sv_rows = []
    for word1, tag1 in synonym_vector1:
        for word2, tag2 in synonym_vector2:
            if word1 == word2:
                score = 1.0
            elif tag1 == tag2 and len(tag1) == 8:
                score = 0.95
            elif tag1 == tag2: # 少于8位时为默认分词属性，不在自定义词典内
                score = 0.40
            elif tag1[:7] == tag2[:7]:
                score = 0.90
            elif tag1[:6] == tag2[:6]:
                score = 0.86
            elif tag1[:5] == tag2[:5]:
                score = 0.83
            elif tag1[:4] == tag2[:4]:
                score = 0.70
            elif tag1[:3] == tag2[:3]:
                score = 0.60
            elif tag1[:2] == tag2[:2]:
                score = 0.50
            elif tag1[:1] == tag2[:1]:
                score = 0.40
            else:
                score = 0.10
            if score < 0.5:
                jscore = jaccard_basic(list(word1), list(word2))
                if jscore >= 0.5:
                    score = jscore
            sv_rows.append(score)
        sv_matrix.append(sv_rows)
        sv_rows = []
    matrix = np.mat(sv_matrix)
    result = sum_cosine(matrix, threshold)
    # result = sum_cosine(matrix, 0.85) # 区分“电脑”和“打印机”：标签前5位相同
    total = result["total"]
    total_dif = result["total_dif"]
    num = result["num_not_match"]
    sim = total/(total + num*(1-total_dif))
    return sim

def edit_distance(synonym_vector1, synonym_vector2):
    """Similarity score between two vectors with edit distance.
    根据语义编辑距离计算相似度。
    """
    sim = 1
    print(synonym_vector1, synonym_vector2)
    # print(str(sim))
    return sim

def similarity(synonym_vector1, synonym_vector2, pattern='j'):
    """Similarity score between two sentences.
    两个向量的相似度得分。

    Args:
        pattern: Similarity computing model. 相似度计算模式。
            Defaults to 'j' represents 'jaccard'.
    """
    assert synonym_vector1 != [], "synonym_vector1 can not be empty"
    assert synonym_vector2 != [], "synonym_vector2 can not be empty"
    if synonym_vector1 == synonym_vector2:
        return 1.0
    if pattern == 'jb':
        sim = jaccard_basic(synonym_vector1, synonym_vector2)
    elif pattern == 'j':
        sim = jaccard(synonym_vector1, synonym_vector2)
    elif pattern == 'j2':
        sim = jaccard2(synonym_vector1, synonym_vector2)
    elif pattern == 'e':
        sim = edit_distance(synonym_vector1, synonym_vector2)
    return sim

def similarity2(s1, s2):
    """Similarity score between two sentences.
    计算两个句子的相似度，得分区间为[0, 1]。
    """
    assert s1 != '', "sentence can not be empty"
    assert s2 != '', "sentence can not be empty"
    if s1 == s2:
        return 1.0
    return jaccard2(segment(s1), segment(s2))

def get_location(sentence):
    """Get location in sentence. 获取句子中的地址。
    """
    location = []
    sv_sentence = synonym_cut(sentence, 'wf')
    for word, tag in sv_sentence:
        if tag.startswith("Di02") or tag.startswith("Di03") or tag == "Cb25A11#":
            location.append(word)
    return location

def get_musicinfo(sentence):
    """Get music info in sentence.
    """
    words = sentence.lstrip("唱一首").split("的")
    singer = words[0]
    song = words[1]
    return (singer, song)
