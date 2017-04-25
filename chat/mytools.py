#!/usr/bin/env python3
# -*- coding:utf8 -*-
# PEP 8 check with Pylint
"""A collection of useful tools. 实用工具集合。

Including batch processing, performance analysis, data analysis, etc..
包含批处理，性能分析，数据分析等。

Available functions:
- All classes and functions: 所有类和函数
"""

import os
import time
import inspect
import random
from functools import wraps
import socket
import uuid
import xlrd
import xlwt

def get_mac_address():
    """Get mac address.
    """
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0, 11, 2)])

def get_hostname():
    """Get hostname.
    """
    return socket.getfqdn(socket.gethostname())

def get_ip_address(hostname):
    """Get ip address.
    """
    return socket.gethostbyname(hostname)

def get_current_function_name():
    """Get current function name.
    """
    return inspect.stack()[1][3]


class Walk():
    """Walk directory to batch processing.
    遍历目录进行批处理。

    Subclasses may override the 'handle_file' method to provide custom file processing mode.
    子类可以重写'handle_file'方法来实现自定义的文件处理方式。

    Public attributes:
    - filelist: All filenames with full path in directory.
    - fnamelist: All filenames in directory.
    - dirlist: All dirnames with full path in directory.
    - dnamelist: All filenames in directory.
    """
    def __init__(self):
        self.filenum = 0
        self.filelist = []
        self.fnamelist = []
        self.dirlist = []
        self.dnamelist = []
        self.dirstr = '+'
        self.filestr = '-'

    def dir_print(self, level, path):
        """Walk and print all dirs and files in a directory.
        遍历目录打印所有子目录及文件名。

        Args:
            level: Level of current directory. 目录的深度。
            path: Full path of current directory. 目录的完整路径。

        Returns:
            filenum. 遍历目录下的所有文件总数。
        """
        files = os.listdir(path)
        # 先添加目录级别
        self.dirlist.append(str(level))
        for file in files:
            if os.path.isdir(path+'/'+file):
                # 排除隐藏文件夹
                if file[0] == '.':
                    pass
                else:
                    self.dirlist.append(file)
            if os.path.isfile(path + '/' + file):
                # 添加文件
                self.filelist.append(file)
        # 文件夹列表第一个级别不打印
        for dirname in self.dirlist[1:]:
            print('-' * (int(self.dirlist[0])), dirname)
            # 递归打印目录下的所有文件夹和文件，目录级别+1
            self.dir_print((int(self.dirlist[0])+1), path+'/'+dirname)
        for filename in self.filelist:
            print('-' * (int(self.dirlist[0])), filename)
            self.filenum = self.filenum + 1
        return self.filenum

    def str_file(self, level):
        """Get str that represents the level of the file.
        文件层级信息的打印字符表示。
        """
        return '  ' * level + self.filestr

    def str_dir(self, level):
        """Get str that represents the level of the directory.
        目录层级信息的打印字符表示。
        """
        return '  ' * level + self.dirstr

    def dir_process(self, level, path, style="fnamelist"):
        """Walk and process all dirs and files in a directory.
        遍历目录批处理所有文件。

        Args:
            level: Level of current directory. 目录的深度。
            path: Full path of current directory. 目录的完整路径。
            style: Specifies the content to return. 指定要返回的内容。
                The style can be 'filelist', 'fnamelist', 'dirlist' or 'dnamelist'.
                Defaults to "fnamelist".

        Returns:
            filenum. 遍历目录下的所有文件总数。
        """
        if os.path.exists(path):
            files = os.listdir(path)
            for file in files:
                # Exclude hidden folders and files
                if file[0] == '.':
                    continue
                else:
                    subpath = os.path.join(path, file)
                if os.path.isfile(subpath):
                    # Get filelist and fnamelist
                    fname = os.path.basename(subpath)
                    self.filelist.append(subpath)
                    self.fnamelist.append(fname)
                    print(self.str_file(level) + fname)
					# Handle file with specified method by pattern
                    self.handle_file(subpath)
                else:
                    leveli = level + 1
                    # Get dirlist and dnamelist
                    dname = os.path.basename(subpath)
                    self.dirlist.append(subpath)
                    self.dnamelist.append(dname)
                    print(self.str_dir(level) + dname)
                    self.dir_process(leveli, subpath, style)
        # Return the specified list by style
        return self.__dict__[style]

    def handle_file(self, filepath, pattern=None):
        """Handle file with specified method by pattern.
        根据pattern指定的模式处理文件。

        Args:
            filepath: Full path of file. 文件的完整路径。
            pattern: Specifies the pattern to handle file. 指定处理该文件的模式。
                Defaults to None.

        Returns:
            You can customize when you override this method. 当你重写该方法时可以自定义。
        """
        print(self.filenum)
        print("filepath=" + filepath)
        print("pattern=" + str(pattern))
        print("Handling...\n")


def time_me(info="used", format_string="ms"):
    """Performance analysis - time

    Decorator of time performance analysis.
    性能分析——计时统计
    系统时间(wall clock time, elapsed time)是指一段程序从运行到终止，系统时钟走过的时间。
    一般系统时间都是要大于CPU时间的。通常可以由系统提供，在C++/Windows中，可以由<time.h>提供。
    注意得到的时间精度是和系统有关系的。
    1.time.clock()以浮点数计算的秒数返回当前的CPU时间。用来衡量不同程序的耗时，比time.time()更有用。
    time.clock()在不同的系统上含义不同。在UNIX系统上，它返回的是"进程时间"，它是用秒表示的浮点数（时间戳）。
    而在WINDOWS中，第一次调用，返回的是进程运行的实际时间。而第二次之后的调用是自第一次
    调用以后到现在的运行时间。（实际上是以WIN32上QueryPerformanceCounter()为基础，它比毫秒表示更为精确）
    2.time.perf_counter()能够提供给定平台上精度最高的计时器。计算的仍然是系统时间，
    这会受到许多不同因素的影响，例如机器当前负载。
    3.time.process_time()提供进程时间。

    Args:
        info: Customize print info. 自定义提示信息。
        format_string: Specifies the timing unit. 指定计时单位，例如's': 秒，'ms': 毫秒。
            Defaults to 's'.
    """
    def _time_me(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            start = time.clock()
            # start = time.perf_counter()
            # start = time.process_time()
            result = func(*args, **kwargs)
            end = time.clock()
            if format_string == "s":
                print("%s %s %s"%(func.__name__, info, end - start), "s")
            elif format_string == "ms":
                print("%s %s %s" % (func.__name__, info, 1000*(end - start)), "ms")
            return result
        return _wrapper
    return _time_me


def get_current_time(format_string="%Y-%m-%d-%H-%M-%S", info=None):
    """Get current time with specific format_string.
    获取指定日期表示方式的当前时间。

    Args:
        format_string: Specifies the format of time. 指定日期表示方式。
            Defaults to '%Y-%m-%d-%H-%M-%S'.
    """
    assert isinstance(format_string, str), "The format_string must be a string."
	# Python3
	# On Windows, time.strftime() and Unicode characters will raise UnicodeEncodeError.
    # http://bugs.python.org/issue8304
    try:
        current_time = time.strftime(format_string, time.localtime())
    except UnicodeEncodeError:
        result = time.strftime(format_string.encode('unicode-escape').decode(), time.localtime())
        current_time = result.encode().decode('unicode-escape')
    return current_time

def random_item(mylist):
    """Get random item of data.
    从数据中获取随机元素。

    Returns:
        item: Random item of data. 数据随机项。
    """
    assert mylist is not None, "The list can not be None."
    if isinstance(mylist, list):
        item = mylist[random.randint(0, len(mylist)-1)]
    elif isinstance(mylist, str):
        item = mylist
    return item

def file_replace(source_file, destination_file):
    """File replace.
    文件替换。

    Args:
        source_file: The full path of source file. 原始文件完整路径。
        destination_file：The full path of destination file. 目标文件完整路径。
    """
    with open(source_file, 'r') as source:
        with open(destination_file, 'w') as destination:
            destination.write(source.read())

def read_excel(filepath):
    """Get excel source

    Args:
        filepath: The full path of excel file. excel文件完整路径。

    Returns:
        data: Data of excel. excel数据。
    """
    is_valid = False
    try:
        if os.path.isfile(filepath):
            filename = os.path.basename(filepath)
            if filename.split('.')[1] == 'xls':
                is_valid = True
        data = None
        if is_valid:
            data = xlrd.open_workbook(filepath)
    except Exception as xls_error:
        raise TypeError("Can't get data from excel!") from xls_error
    return data

def set_excel_style(name, height, bold=False):
    """Set excel style.
    """
    style = xlwt.XFStyle() # 初始化样式
    font = xlwt.Font() # 为样式创建字体
    font.name = name # 例如'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height
    if bold:
        borders = xlwt.Borders()
        borders.left = 6
        borders.right = 6
        borders.top = 6
        borders.bottom = 6
        style.borders = borders
    style.font = font
    return style

def write_excel(filename="demo.xlsx", sheets=None):
    """Write excel from data.
    """
    file = xlwt.Workbook() # 创建工作簿
    for sheet in sheets:
        new_sheet = file.add_sheet(sheet["name"], cell_overwrite_ok=True) # 创建sheet
        # 生成表头
        new_sheet.write(0, 0, "version=1.0.0", set_excel_style('Arial Black', 220, True))
        for col, key in enumerate(sheet["keys"]):
            new_sheet.write(1, col, key, set_excel_style('Arial Black', 220, True))
        # 生成内容
        for index, item in enumerate(sheet["items"]):
            for col, key in enumerate(sheet["keys"]):
                new_sheet.write(index+2, col, item['n'][key])
    file.save(filename) # 保存文件

def generate_dict(dictpath, sourcepath):
    """Generate dictionary file from sourcefile.

    Args:
        dictpath: The full path of dict file. 源文件完整路径。
        sourcepath: The full path of source file. 源文件完整路径。
    """
    assert dictpath is not None, "The dictpath can not be None."
    assert sourcepath is not None, "The sourcepath can not be None."
    with open(dictpath, 'w', encoding="UTF-8") as new:
        with open(sourcepath, 'r', encoding="UTF-8") as file:
            for line in file:
                content = line.split()
                tag = content[0]
                for word in content[1:]:
                    new.write(word + " 2000 " + tag + "\n")

def waitting():
    """Print waitting.
    """
    while True:
        for i in ["/", "*", "|", "\\", "|"]:
            print("%s\r" % i, end="")
            time.sleep(0.3)
