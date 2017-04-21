#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from unittest import TestCase, main
from chat.mytools import get_current_time
from chat.semantic import synonym_cut, similarity

class TestMe(TestCase):
    def setUp(self):
        self.semantic = None

    def test_jaccard(self):
        print("语义相似度测试......")
        filename = ".\\log\\SemanticSimilarity_" + get_current_time() + ".md"
        file = open(filename, "w")
        file.write("标签：测试文档\n#向量语义相似度测试：\n>Enter the SemanticSimilarity mode...\n")
        while True:
            try:
                sentence1 = input("\nsentence1\n>>")
                sentence2 = input("sentence2\n>>")
                sv1 = synonym_cut(sentence1, 'wf')
                sv2 = synonym_cut(sentence2, 'wf')
                print(sv1, sv2)
                sim = similarity(sv1, sv2)
                file.write("`>>" + sentence1 + "`\n")
                file.write("`>>" + sentence2 + "`\n")
                print("words similarity: " + str(sim))
                file.write("`" + "words similarity: " + str(sim) + "`\n")
            except KeyboardInterrupt:
                file.close()


if __name__ == '__main__':
    main()
