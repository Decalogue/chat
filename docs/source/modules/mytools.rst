API - 常用工具箱
========================

.. image:: my_figs/mytools.ico
  :scale: 50 %

.. automodule:: chat.mytools

.. autosummary::

   mytools.Error
   mytools.StringPatternError
   mytools.MyEncoder
   mytools.get_mac_address
   mytools.get_hostname
   mytools.get_ip_address
   mytools.get_host_ip
   mytools.get_current_function_name
   mytools.Walk
   mytools.time_me
   mytools.get_timestamp
   mytools.get_current_time
   mytools.get_age
   mytools.random_item
   mytools.file_replace
   mytools.read_excel
   mytools.set_excel_style
   mytools.write_excel
   mytools.write_excel_sql
   mytools.generate_dict
   mytools.waitting

自定义异常
------------------------
.. autofunction:: mytools.Error

自定义字符串格式异常
------------------------
.. autofunction:: mytools.StringPatternError

MyEncoder 解决 json.dumps 不能序列化 datetime 类型的问题
------------------------
.. autofunction:: mytools.MyEncoder
   
获取Mac地址
------------------------
.. autofunction:: mytools.get_mac_address

获取主机名
------------------------
.. autofunction:: mytools.get_hostname

获取IP地址
------------------------
.. autofunction:: mytools.get_ip_address
.. autofunction:: mytools.get_host_ip

获取当前运行函数名
------------------------
.. autofunction:: mytools.get_current_function_name

遍历目录进行批处理
------------------------
.. autofunction:: mytools.Walk

程序时间性能分析
------------------------
.. autofunction:: mytools.time_me

获取指定日期表示方式的时间戳或者当前时间戳
------------------------
.. autofunction:: mytools.get_timestamp

获取指定日期表示方式的当前时间
------------------------
.. autofunction:: get_current_time

获取指定日期表示方式的年龄
------------------------
.. autofunction:: mytools.get_age

列表随机元素
------------------------
.. autofunction:: mytools.random_item

文件替换
------------------------
.. autofunction:: mytools.file_replace

读取excel
------------------------
.. autofunction:: mytools.read_excel

设置excel样式
------------------------
.. autofunction:: mytools.set_excel_style

写入excel
------------------------
.. autofunction:: mytools.write_excel
.. autofunction:: mytools.write_excel_sql

生成词典
------------------------
.. autofunction:: mytools.generate_dict

显示等待中
------------------------
.. autofunction:: mytools.waitting
