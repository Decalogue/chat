#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from unittest import TestCase, main
from chat.database import Database
from chat.mytools import time_me

class TestMe(TestCase):
    def setUp(self):
        self.database = Database(password="train")

    def test_delete(self):
        pass

    def test_reset(self):
        # self.database.reset(pattern="n", label="NluCell", filename="C:/rain/cloud/one/data/one.xls")
        self.database.reset(pattern="n", label="NluCell", filename="C:/nlu/data/chat.xls")
    @time_me(format_string="ms")
    def test_add_qa(self):
        pass
        # 1.Add qa with excel
        # self.database.handle_excel("C:/nlu/data/chat.xls")
	    # 2.Add qa with txt
        # self.database.handle_txt("C:/nlu/data/bank.txt")
    
    def test_register_subgraph(self):
        pass
        # print(self.database.gconfig)
        # self.database.register_subgraph(name="新命令", topic="new_chat")

    def test_register_user(self):
        pass
        # self.database.register_user()

    def test_manage_user(self):
        pass
        # self.database.manage_user(userid="test", name="基础问答")


if __name__ == '__main__':
    main()
