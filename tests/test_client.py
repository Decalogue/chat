#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("../")
import json
from unittest import TestCase, main
from chat.client import match
from chat.mytools import get_current_time

class TestMe(TestCase):
    def setUp(self):
        self.username = "username"

    def test_match(self):
        filename = os.path.split(os.path.realpath(__file__))[0] + "\\log\\QA_" + get_current_time() + ".md"
        file = open(filename, "w")
        file.write("标签：测试文档\n#QA测试：\n>Enter the QA mode...\n")
        sentence = ""
        result = ""
        while True:
            try:
                sentence = input("\n>>")
                if sentence == "":
                    break
                result = match(question=sentence, username=self.username)
                answer = json.loads(result)["content"]
                print(answer)
                file.write("`>>" + sentence + "`\n")
                file.write("`" + "A: " + answer + "`\n")
            except KeyboardInterrupt:
                file.close()


if __name__ == '__main__':
    main()
