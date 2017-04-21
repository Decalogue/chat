#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from unittest import TestCase, main
from chat.mytools import get_current_time
from chat.vec import Vec

class TestMe(TestCase):
    def setUp(self):
        self.vec = Vec()

    def test_jaccard(self):
        print("向量语义相似度测试......")
        filename = "\\log\\VecSimilarity_" + get_current_time() + ".md"
        file = open(filename, "w")
        file.write("标签：测试文档\n#向量语义相似度测试：\n>Enter the VecSimilarity mode...\n")
        while True:
            try:
                sentence1 = input("\nsentence1\n>>")
                sentence2 = input("sentence2\n>>")
                file.write("`>>" + sentence1 + "`\n")
                file.write("`>>" + sentence2 + "`\n")
                similarity = self.vec.jaccard(sentence1, sentence2)
                print("words similarity: " + str(similarity))
                file.write("`" + "words similarity: " + str(similarity) + "`\n")

                self.vec.pattern = "t"
                similarity = self.vec.jaccard(sentence1, sentence2)
                print("tags similarity: " + str(similarity))
                file.write("`" + "tags similarity: " + str(similarity) + "`\n")
            except KeyboardInterrupt:
                file.close()


if __name__ == '__main__':
    main()
