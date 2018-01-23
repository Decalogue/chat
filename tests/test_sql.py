# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from unittest import TestCase, main
from chat.sql import Database
from chat.mytools import Walk, time_me


class WalkUserData(Walk):
    def handle_file(self, filepath, pattern=None):
        self.db.handle_excel(filepath)


class TestMe(TestCase):
    def setUp(self):
        self.database = Database(path='C:/nlu/data/db/nlu_sqlite.db', userid="A0001")
        
    def test_add_userdata(self):
        """Add userdata from usb.
        """
        # path = "D:/新知识库"
        # walker = WalkUserData(db=self.database)
        # fnamelist = walker.dir_process(1, path, style="fnamelist")
        pass
            
    def test_drop_table(self):
        print('删除数据库表测试...')
        for table in ['User', 'Config', 'NluCell']:
            self.database.drop_table(table)

    def test_create_table(self):
        print('创建数据库表测试...')
        self.database.create_table_user()
        self.database.create_table_config()
        self.database.create_table_nlucell()
        # pass

    def test_get_user(self):
        print('获取 User 测试...')
        self.database.get_user()
        # pass
        
    def test_add_config(self):
        print('添加 Config 测试...')
        add_config = '''INSERT INTO Config values (?, ?, ?, ?, ?)'''
        config = [(1, 'A0001', '银行业务', '', '1'),
                (2, 'A0001', '闲聊', '', '1'),
                (3, 'A0002', '银行业务', '', '1')]
        self.database.update(add_config, config)
        # pass
        
    def test_add_nlucell(self):
        print('添加 NluCell 测试...')
        self.database.handle_excel('C:/nlu/data/kb/chat.xls')
        print('可用知识库：', self.database.get_available_kb())
        print('已挂接知识库：', self.database.get_selected_kb())
        # pass
        
    def test_reset(self):
        print('重置 NluCell 测试...')
        self.database.reset(tabel='NluCell', filename='C:/nlu/data/kb/chat.xls')
        # pass

    # @time_me(format_string="ms")
    def test_add_qa(self):
        pass
        # Add qa with excel
        # self.database.handle_excel("C:/nlu/data/kb/chat.xls")
    
    def test_download(self):
        akbs = self.database.get_available_kb()
        print('下载 NluCell 测试...')
        self.database.download(filename='C:/nlu/data/download/chat_sql.xls', names=akbs)
        # pass

    def test_generate_test_cases(self):
        # self.database.generate_test_cases(
            # filename='C:/nlu/data/kb/chat.xls',
            # custom_sheets=["银行业务"],
            # savedir="."
        # )
        pass


if __name__ == '__main__':
    main()
