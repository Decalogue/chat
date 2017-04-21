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

    @time_me(format_string="ms")
    def test_add_qa(self):
        pass
        # 1.Add qa with excel
        self.database.handle_excel("C:/nlu/data/chat.xls")
	    # 2.Add qa with txt
        # self.database.handle_txt("C:/nlu/data/bank.txt")


if __name__ == '__main__':
    main()
