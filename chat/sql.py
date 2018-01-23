# -*- coding: utf-8 -*-
"""NLU Database Manager.
自然语言理解知识库管理。
"""
import os
import sqlite3
import string
from tkinter.filedialog import askopenfilename
from .mytools import read_excel, write_excel_sql
from .semantic import get_tag


class Database():
    """Manage Database.
    管理知识库。

    Public attributes:
    - conn: Connection object to the database. 数据库连接对象。
    - cu: Cursor object of the database. 数据库游标对象。
    - show_sql: Whether or not to show sql. 是否显示数据库操作过程。
    """
    def __init__(self, path='', sql=sqlite3, userid="A0001", show_sql=False):
        self.path = path
        self.sql = sql
        self.conn = self.get_conn()
        self.cu = self.get_cursor()
        self.show_sql = show_sql
        self.skb = ''
        self.dkb = []
        self.userid = userid
        self.user = self.get_user()
        if not self.user:
            self.add_user()
            self.user = self.get_user()
        
    def get_conn(self):
        '''Get the connection object to the database.
        获取到数据库的连接对象。

        Args:
            path: 数据库文件的绝对路径。
                Defaults to None.
            sql: 数据库类型。
                Defaults to sqlite3.
        '''
        if os.path.exists(self.path) and os.path.isfile(self.path):
            print('硬盘上面:[{}]'.format(self.path))
            db = self.path
        else:
            print('内存上面:[:memory:]')
            db = ':memory:'
        try:
            conn = self.sql.connect(db, check_same_thread=False)
        except:
            conn = None
        return conn

    def get_cursor(self):
        '''Get the cursor object of the database.
        获取数据库的游标对象。

        Args:
            conn: 数据库连接对象。
                Defaults to None.
        '''
        if self.conn is not None:
            return self.conn.cursor()
        else:
            return self.get_conn().cursor()

    def close_all(self):
        '''关闭数据库游标对象和数据库连接对象'''
        try:
            if self.cu is not None:
                self.cu.close()
        finally:
            if self.conn is not None:
                self.conn.close()

    def drop_table(self, table):
        '''删除表（如果表存在），表中存在数据时，要慎用该方法！
        
        Args:
            table：数据库表名。
        '''
        if table is not None and table != '':
            sql = 'DROP TABLE IF EXISTS ' + table
            if self.show_sql:
                print('执行sql:[{}]'.format(sql))
            # cu = get_cursor(conn)
            self.cu.execute(sql)
            self.conn.commit()
            print('删除数据库表[{}]成功!'.format(table))
            # self.close_all(self.conn, self.cu)
        else:
            print('The [{}] is empty or equal None!'.format(sql))

    def create_table(self, sql):
        '''创建数据库表'''
        if sql is not None and sql != '':
            # cu = get_cursor(conn)
            if self.show_sql:
                print('执行sql:[{}]'.format(sql))
            self.cu.execute(sql)
            self.conn.commit()
            print('创建数据库表成功!')
            # self.close_all(self.conn, self.cu)
        else:
            print('The [{}] is empty or equal None!'.format(sql))

    def create_table_user(self):
        user = '''CREATE TABLE `User` (
            `userid` varchar(100) NOT NULL,
            `robotname` varchar(100) NOT NULL,
            `robotage` varchar(100) NOT NULL,
            `robotgender` varchar(100) NOT NULL,
            `mother` varchar(100) NOT NULL,
            `father` varchar(100) NOT NULL,
            `username` varchar(100) NOT NULL,
            `companyname` varchar(100) NOT NULL,
            `companytype` varchar(100) NOT NULL,
            `servicename` varchar(100) NOT NULL,
            `director` varchar(100) NOT NULL,
            `address` varchar(100) NOT NULL,
            `province` varchar(100) NOT NULL,
            `city` varchar(100) NOT NULL,
            `self_intro` varchar(100) NOT NULL,
            `company_intro` varchar(100) NOT NULL,
            `error_page` varchar(100) NOT NULL,
             PRIMARY KEY (`userid`)
        )'''
        self.create_table(user)

    def create_table_config(self):
        config = '''CREATE TABLE `Config` (
            `id` int(11) NOT NULL,
            `userid` varchar(100) NOT NULL,
            `name` varchar(100) NOT NULL,
            `topic` varchar(200) NOT NULL,
            `bselected` varchar(200) NOT NULL,
             PRIMARY KEY (`id`)
        )'''
        self.create_table(config)

    def create_table_nlucell(self):
        nlucell = '''CREATE TABLE `NluCell` (
            `id` int(11) NOT NULL,
            `name` varchar(100) NOT NULL,
            `content` varchar(200) NOT NULL,
            `topic` varchar(200) NOT NULL,
            `tid` int(10) NOT NULL,
            `ftid` int(10) NOT NULL,
            `behavior` varchar(200) NOT NULL,
            `parameter` varchar(200) NOT NULL,
            `url` varchar(200) NOT NULL,
            `tag` varchar(200) NOT NULL,
            `keywords` varchar(200) NOT NULL,
            `api` varchar(200) NOT NULL,
            `txt` varchar(200) NOT NULL,
            `img` varchar(200) NOT NULL,
            `button` varchar(200) NOT NULL,
            `description` varchar(200) NOT NULL,
            `hot` varchar(200) NOT NULL,
             PRIMARY KEY (`id`)
        )'''
        self.create_table(nlucell)

    def fetch(self, sql, data=None):
        '''查询数据'''
        if sql is not None and sql != '':
            if data is not None:
                # cu = get_cursor(conn)
                if self.show_sql:
                    print('执行sql:[{}],参数:[{}]'.format(sql, data))
                self.cu.execute(sql, data)
                result = self.cu.fetchall()
                # self.close_all(self.conn, self.cu)
                if result:
                    # print(result)
                    return result
            else:
                print('The [{}] equal None!'.format(data))
        else:
            print('The [{}] is empty or equal None!'.format(sql))
        return None

    def fetchall(self, sql):
        '''查询所有数据'''
        if sql is not None and sql != '':
            # cu = get_cursor(conn)
            if self.show_sql:
                print('执行sql:[{}]'.format(sql))
            self.cu.execute(sql)
            result = self.cu.fetchall()
            # self.close_all(self.conn, self.cu)
            if result:
                # print(result)
                return result
        else:
            print('The [{}] is empty or equal None!'.format(sql))
        return None

    def fetchone(self, sql, data=None):
        '''查询唯一一条数据'''
        if sql is not None and sql != '':
            if data is not None:
                #Do this instead
                d = (data,) 
                # cu = get_cursor(conn)
                if self.show_sql:
                    print('执行sql:[{}],参数:[{}]'.format(sql, data))
                self.cu.execute(sql, d)
                result = self.cu.fetchall()
                # self.close_all(self.conn, self.cu)
                if result:
                    # print(result)
                    return result
            else:
                print('The [{}] equal None!'.format(data))
        else:
            print('The [{}] is empty or equal None!'.format(sql))
        return None

    def fetchtable(self, table=''):
        '''查询子表数据'''
        sql = 'SELECT * FROM ' + table
        result = self.fetchall(sql)
        return result

    def update(self, sql, data=None):
        '''更新数据'''
        if sql is not None and sql != '':
            if data is not None:
                # cu = get_cursor(conn)
                for d in data:
                    if self.show_sql:
                        print('执行sql:[{}],参数:[{}]'.format(sql, d))
                    self.cu.execute(sql, d)
                    self.conn.commit()
                # self.close_all(self.conn, self.cu)
        else:
            print('The [{}] is empty or equal None!'.format(sql))

    def delete(self, sql, data=None):
        '''删除数据'''
        if sql is not None and sql != '':
            if data is not None:
                # cu = get_cursor(conn)
                for d in data:
                    if self.show_sql:
                        print('执行sql:[{}],参数:[{}]'.format(sql, d))
                    self.cu.execute(sql, d)
                    self.conn.commit()
                # self.close_all(self.conn, self.cu)
        else:
            print('The [{}] is empty or equal None!'.format(sql))

    def delete_nlucell_item(self, data=None):
        '''根据 topic 和 tid 删除 NluCell'''
        sql = 'DELETE FROM NluCell WHERE topic = ? AND tid = ? '
        self.delete(sql, data)

    def delete_tabel_data(self, tabel=''):
        '''删除 tabel 对应的全部数据'''
        sql = 'DELETE FROM ' + tabel
        self.cu.execute(sql)
        self.conn.commit()
        
    def add_user(self, data=None):
        sql = '''INSERT INTO User values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        if not data:
            data = [(['A0001', 'robotname', 'robotage', 'robotgender', 'mother', 'father', 
                'username', 'companyname', 'companytype', 'servicename', 'director', 
                'address', 'province', 'city', 'self_intro', 'company_intro', 'error_page'])]
        self.update(sql, data)
    
    def get_user(self, userid=None):
        if not userid:
            userid = self.userid
        sql = 'SELECT * FROM User WHERE userid = ? '
        try:
            result = self.fetchone(sql, userid)[0]
        except:
            return None
        user = {}
        keys = ['userid', 'robotname', 'robotage', 'robotgender', 'mother', 'father', 
                'username', 'companyname', 'companytype', 'servicename', 'director', 
                'address', 'province', 'city', 'self_intro', 'company_intro', 'error_page']
        for index, key in enumerate(keys):
            user[key] = result[index]
        return user

    def get_config(self, userid=None, name=''):
        if not userid:
            userid = self.userid
        if name != '':
            sql = 'SELECT * FROM Config WHERE userid = ? and name = ?'
            return self.fetch(sql, data=(userid, name))
        else:
            sql = 'SELECT * FROM Config WHERE userid = ?'
            return self.fetch(sql, data=(userid,))

    def reset(self, tabel=None, filename=None):
        """Reset data of tabel in database.
        重置子数据库。

        Args:
            tabel: Tabel of database. 知识库表名。
        """ 
        assert filename is not None, "filename can not be None."
        self.delete_tabel_data(tabel=tabel)
        print("Delete successfully!")
        if os.path.exists(filename):
            self.handle_excel(filename)
        else:
            print("You can set 'filename=<filepath>' when you call 'Database.reset.'")
        print("Reset successfully!")

    def add_nlucell(self, id=None, name=None, content=None, topic="", tid="", \
        ftid="", behavior="", parameter="", url="", tag="", keywords="", api="", txt="", \
        img="", button="", description="", hot='0', delimiter=None):
        """
        Add nlucell.
        """
        assert name is not None, "name must be string."
        assert content is not None, "content must be string."
        sql = '''INSERT INTO NluCell values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        questions = name.split(delimiter)
        for question in questions:
            if question: # 问题不能为空，避免因知识库表格填写格式不对而导致存入空问答对
                tag = get_tag(question, self.user)
                data = [(id, question, content, topic, tid, ftid, behavior, parameter, url, tag, keywords, api, txt, img, button, description, hot)]
                self.update(sql, data)

    def handle_excel(self, filename=None, custom_sheets=[]):
        """Processing data of excel.
        """
        assert filename is not None, "filename can not be None"
        data = read_excel(filename)
        data_sheets = data.sheet_names()
        if custom_sheets:
            sheet_names = list(set(data_sheets).intersection(set(custom_sheets)))
        else:
            sheet_names = data_sheets
        id = 1
        for sheet_name in sheet_names: # 可自定义要导入的子表格
            table = data.sheet_by_name(sheet_name)
            topics = []
            # 1.Select specified table
            # table = data.sheet_by_index(0)
            if data:
                # 2.Select specified column
                col_format = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
                try:
                    nrows = table.nrows
                    # ncols = table.ncols
                    str_upcase = [i for i in string.ascii_uppercase]
                    i_upcase = range(len(str_upcase))
                    ncols_dir = dict(zip(str_upcase, i_upcase))
                    col_index = [ncols_dir.get(i) for i in col_format]
                    # 前两行为表头
                    for i in range(2, nrows):
                        name = table.cell(i, col_index[0]).value
                        content = table.cell(i, col_index[1]).value
                        # Modify：2018-1-17
                        # 场景 topic 必须填写，问答 topic 可不填，若填写必须为 sheet_name
                        temp = table.cell(i, col_index[2]).value
                        topic =  temp if temp else sheet_name
                        tid = table.cell(i, col_index[3]).value
                        ftid = table.cell(i, col_index[4]).value
                        behavior = table.cell(i, col_index[5]).value
                        parameter = table.cell(i, col_index[6]).value
                        url = table.cell(i, col_index[7]).value
                        tag = table.cell(i, col_index[8]).value
                        keywords = table.cell(i, col_index[9]).value
                        api = table.cell(i, col_index[10]).value
                        txt = table.cell(i, col_index[11]).value
                        img = table.cell(i, col_index[12]).value
                        button = table.cell(i, col_index[13]).value
                        description = table.cell(i, col_index[14]).value
                        # hot = 0 table.cell(i, col_index[15]).value
					    # 3.Your processing function of excel data here
                        self.add_nlucell(id=id, name=name, content=content, topic=topic, \
                            tid=tid, ftid=ftid, behavior=behavior, parameter=parameter, \
                            url=url, tag=tag, keywords=keywords, api=api, txt=txt, img=img, \
                            button=button, description=description, delimiter="|")
                        id += 1
                        # 添加到场景标签列表
                        if topic:
                            topics.append(topic)
                except Exception as error:
                    print('Error: %s' %error)
                    return None
            else:
                print('Error! Data of %s is empty!' %sheet_name)
                return None
            # 若导入的 excel 子表格名字不存在，在数据库中新建知识库，否则只修改已有知识库的 topic 属性
            config = self.get_config(name=sheet_name)[0]
            alltopics = config[3].split(",") if config[3] else []
            alltopics.extend(topics)
            sql = 'UPDATE Config SET topic = ? WHERE userid = ? and name = ?'
            self.update(sql, data=[(",".join(set(alltopics)), self.userid, sheet_name)])

    def get_available_kb(self, userid=None):
        if not userid:
            userid = self.userid
        kb = []
        sql = 'SELECT * FROM Config WHERE userid = ? '
        for item in self.fetch(sql, data=(userid,)):
            kb.append(item[2])
        return kb
    
    def get_selected_kb(self, userid=None):
        if not userid:
            userid = self.userid
        sql = 'SELECT * FROM Config WHERE userid = ? and bselected = ?'
        config = self.fetch(sql, data=(userid, '1'))
        kb = [item[2] for item in config] if config else []
        return kb

    def download(self, filename=None, names=[]):
        """下载知识库
        """
        assert filename is not None, "Filename must be *.xls!"
        assert names is not [], "Subgraph names can not be empty!"
        sql = "SELECT * FROM NluCell WHERE topic = ?"
        # Modify：使键值按照指定顺序导出 excel (2018-1-8)
        info = [('name', '问题'), ('content', '回答'), ('topic', '场景标签'), ('tid', '场景ID'),
            ('ftid', '父场景ID'), ('behavior', '行为'), ('parameter', '动作参数'), ('url', '资源'), 
            ('tag', '语义标签'), ('keywords', '关键词'), ('api', '内置功能'), ('txt', '显示文本'), 
            ('img', '显示图片'), ('button', '显示按钮'), ('description', '场景描述'), ("hot", '搜索热度')]
        # Modify：若采用字典，可用如下方案(2018-1-9)
        # import collections
        # info = collections.OrderedDict(info)
        sheets = []
        
        for name in names:
            config = self.get_config(name=name)[0]
            topics = config[3].split(",") if config else []
            items = []
            for topic in topics:
                item = self.fetch(sql, data=(topic,))
                items.extend(item)
            sheets.append({"name": name, "info": info, "items": items})
            
        write_excel_sql(filename=filename, sheets=sheets)
    
    def upload(self, names=[]):
        """上传知识库
        """
        filename = askopenfilename(filetypes=[('知识库', '*.xls')])
        self.handle_excel(filename, custom_sheets=names)


if __name__ == '__main__':
    db = Database(path='C:/nlu/data/db/nlu_sqlite.db', sql=sqlite3, userid="A0001")
    
    print('删除数据库表测试...')
    for table in ['User', 'Config', 'NluCell']:
        db.drop_table(table)
        
    print('创建数据库表测试...')
    db.create_table_user()
    db.create_table_config()
    db.create_table_nlucell()
    
    print('添加 User 测试...')
    db.add_user()
    
    print('添加 Config 测试...')
    add_config = '''INSERT INTO Config values (?, ?, ?, ?, ?)'''
    config = [(1, 'A0001', '银行业务', '', '1'),
            (2, 'A0001', '闲聊', '', '1'),
            (3, 'A0002', '银行业务', '', '1')]
    db.update(add_config, config)
    
    print('添加 NluCell 测试...')
    db.handle_excel('C:/nlu/data/kb/chat.xls')
    print('可用知识库：', db.get_available_kb())
    print('已挂接知识库：', db.get_selected_kb())
    
    print('重置 NluCell 测试...')
    db.reset(tabel='NluCell', filename='C:/nlu/data/kb/chat.xls')
    
    print('下载 NluCell 测试...')
    db.download(filename='C:/nlu/data/download/chat_sql.xls', names=db.get_available_kb())
