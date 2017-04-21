#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from unittest import TestCase, main
from chat.mytools import *

class TestMe(TestCase):
    def setUp(self):
        self.walk = Walk()

    @time_me(format_string="ms")
    def test_get_current_time(self):
        print(get_current_time())
		
    def test_walk_handle_file(self):
        path = "./"
        self.walk.dir_process(1, path, style="filelist")


if __name__ == '__main__':
    main()
