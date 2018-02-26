# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from unittest import TestCase, main
from chat.graph import Database
from chat.mytools import Walk, time_me


class WalkUserData(Walk):
    def handle_file(self, filepath, pattern=None):
        self.db.handle_excel(filepath)


class TestMe(TestCase):
    def setUp(self):
        self.database = Database(password="train", userid="A0001")
        
    def test_add_userdata(self):
        """Add userdata from usb.
        """
        # path = "D:/新知识库"
        # walker = WalkUserData(db=self.database)
        # fnamelist = walker.dir_process(1, path, style="fnamelist")
        pass

    def test_delete(self):
        pass

    def test_reset(self):
        self.database.reset(pattern="n", label="NluCell", filename="C:/nlu/data/kb/chat.xls")
        # self.database.reset(pattern="n", label="NluCell", filename="C:/nlu/data/kb/chat2.xls")
        # self.database.handle_excel(filename="C:/nlu/data/kb/chat2.xls")
        # pass
 
    def test_reset_ts(self):
        """Reset data of label 'TestStandard' in database.
        """
        # self.database.reset_ts(pattern="n", label="TestStandard", filename="C:/nlu/data/kb/ts.xls")
        pass

    def test_add_ts(self):
        pass
        # self.database.handle_ts("C:/nlu/data/kb/ts.xls")

    # @time_me(format_string="ms")
    def test_add_qa(self):
        pass
        # 1.Add qa with excel
        # self.database.handle_excel("C:/nlu/data/kb/chat.xls")
	    # 2.Add qa with txt
        # self.database.handle_txt("C:/nlu/data/kb/bank.txt")
    
    def test_download(self):
        # akbs = self.database.get_available_kb()
        # self.database.download(filename="全部.xls", names=akbs)
        # self.database.download(filename="银行业务.xls", names=["银行业务"])
        # self.database.download_scene(filename="理财产品.xls", topic="理财产品")
        pass

    def test_generate_test_cases(self):
        # self.database.generate_test_cases(
            # filename="chat.xls",
            # custom_sheets=["银行业务"],
            # savedir="."
        # )
        pass


if __name__ == '__main__':
    main()
