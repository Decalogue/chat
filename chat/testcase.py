#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PEP 8 check with Pylint
import string
import xlwt
from py2neo import Graph, Node, Relationship
from .mytools import read_excel, set_excel_style

graph = Graph("http://localhost:7474/db/data/", password="train")
gconfig = graph.find_one("User", "userid", "A0001")

def generate_test_cases(filename=None, custom_sheets=None):
    """Generating test cases from data of excel.
    
    custom_sheets 选择的子表格集合
    """
    assert filename is not None, "filename can not be None"
    data = read_excel(filename) # 读取已有excel-知识库
    data_sheets = data.sheet_names()
    if custom_sheets:
        sheet_names = list(set(data_sheets).intersection(set(custom_sheets)))
    else:
        sheet_names = data_sheets
        
    file = xlwt.Workbook() # 创建新excel-测试用例
    new_sheet = file.add_sheet("NluTest", cell_overwrite_ok=True) # 创建sheet
    keys = ["问题", "答案", "是否通过", "改进建议"]
    # 生成表头
    new_sheet.write(0, 0, "本地语义常见命令问答测试", set_excel_style('Arial Black', 220, True))
    for col, key in enumerate(keys):
        new_sheet.write(1, col, key, set_excel_style('Arial Black', 220, True))
    count = 0
    testlist = []
    # 生成内容       
    for sheet_name in sheet_names:
        table = data.sheet_by_name(sheet_name)
        # 1.Select specified table
        # table = data.sheet_by_index(0)
        if data:
            # 2.Select specified column
            col_format = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
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
                    questions = name.format(**gconfig).split("|")
                    answers = content.format(**gconfig).split("|")
                    testlist.extend(questions)
                    new_sheet.write(i+count, 0, "\n".join(questions))
                    new_sheet.write(i+count, 1, "\n".join(answers))
                count += nrows - 2
            except Exception as error:
                print('Error: %s' %error)
                return None
        else:
            print('Error! Data of %s is empty!' %sheet_name)
            return None
    file.save("testcase.xls") # 保存文件
    with open("testcase.txt", 'w', encoding="UTF-8") as new:
        for item in testlist:
            new.write(item + "\n")
