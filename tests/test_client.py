# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("../")
import json
from unittest import TestCase, main
from chat.client import match, config, batch_test
from chat.mytools import get_current_time

class TestMe(TestCase):
    def setUp(self):
        self.userid = "A0001"

    def test_match(self):
        # sentences = ['理财产品', '你好', '理财产品取号', '退出', '你好']
        # for sentence in sentences:
            # result = match(question=sentence, userid=self.userid)
            # print(sentence, ':\n', result)
        
        pass
    
    def test_config(self):
        result = json.loads(config(info="", userid="A0001"))
        databases = result.setdefault('databases', [])
        akbs = [item['name'] for item in databases if item['available']==1 ]
        print('akbs: ', akbs)
        skbs = [item['name'] for item in databases if item['bselected']==1 ]
        print('skbs: ', skbs)
        
        # result = config(info=' '.join(skbs[:-1]), userid="A0001")
        result = config(info=' '.join(akbs), userid="A0001")
        print('config: ', result)
        result = json.loads(config(info="", userid="A0001"))
        databases = result.setdefault('databases', [])
        akbs = [item['name'] for item in databases if item['available']==1 ]
        print('akbs: ', akbs)
        skbs = [item['name'] for item in databases if item['bselected']==1 ]
        print('skbs: ', skbs)
        
        pass
        
    def test_batch_test(self):
        # batch_test("testcase.txt")
        pass

if __name__ == '__main__':
    main()
