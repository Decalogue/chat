API - 常用工具箱
========================

.. image:: my_figs/mytools.ico 
.. automodule:: chat.mytools

.. autosummary::

   Error
   StringPatternError
   MyEncoder
   get_mac_address
   get_hostname
   get_ip_address
   get_host_ip
   get_current_function_name
   Walk
   time_me
   get_timestamp
   get_current_time
   get_age
   random_item
   file_replace
   read_excel
   set_excel_style
   write_excel
   write_excel_sql
   generate_dict
   waitting

自定义异常
------------------------
.. autofunction:: Error

自定义字符串格式异常
------------------------
.. autofunction:: StringPatternError

MyEncoder 解决 json.dumps 不能序列化 datetime 类型的问题
------------------------
.. autofunction:: MyEncoder
   
获取Mac地址
------------------------
.. autofunction:: get_mac_address

获取主机名
------------------------
.. autofunction:: get_hostname

获取IP地址
------------------------
.. autofunction:: get_ip_address
.. autofunction:: get_host_ip

获取当前运行函数名
------------------------
.. autofunction:: get_current_function_name

遍历目录进行批处理
------------------------
.. autofunction:: Walk

程序时间性能分析
------------------------
.. autofunction:: time_me

获取指定日期表示方式的时间戳或者当前时间戳
------------------------
.. autofunction:: get_timestamp

获取指定日期表示方式的当前时间
------------------------
.. autofunction:: get_current_time

获取指定日期表示方式的年龄
------------------------
.. autofunction:: get_age

列表随机元素
------------------------
.. autofunction:: random_item

文件替换
------------------------
.. autofunction:: file_replace

读取excel
------------------------
.. autofunction:: read_excel

设置excel样式
------------------------
.. autofunction:: set_excel_style

写入excel
------------------------
.. autofunction:: write_excel
.. autofunction:: write_excel_sql

生成词典
------------------------
.. autofunction:: generate_dict

显示等待中
------------------------
.. autofunction:: waitting
