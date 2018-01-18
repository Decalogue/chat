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
	
    @time_me(format_string="ms")	
    def test_walk_handle_file(self):
        path = "./"
        self.walk.dir_process(1, path, style="filelist")
    
    def test_get_timestamp(self):
        print(get_timestamp())
        print(get_timestamp(pattern='s'))
        print(get_timestamp(pattern='ms'))
        print(get_timestamp(s='2018-1-4 11:23:45'))
        print(get_timestamp(s='2018-1-4 11:23:45', pattern='s'))
        print(get_timestamp(s='2018-1-4 11:23:45', pattern='ms'))
        print(get_timestamp(s='2018-1-4-11-23-45', style='%Y-%m-%d-%H-%M-%S', pattern='ms'))


if __name__ == '__main__':
    main()
