API - 第三方 API 接口
========================

.. image:: my_figs/apilib.png
  :scale: 50 %

.. automodule:: chat.apilib

.. autosummary::

   apilib.nlu_tuling
   apilib.get_location_by_ip
   apilib.get_ll_by_address
   apilib.get_location_by_ll
   apilib.down_mp3_by_url
   apilib.music_baidu
   
图灵 API 接口
------------------------
.. autofunction:: apilib.nlu_tuling

根据IP获取当前地址
------------------------
.. autofunction:: apilib.get_location_by_ip

根据地址获取经纬度
------------------------
.. autofunction:: apilib.get_ll_by_address

根据经纬度获取地址
------------------------
.. autofunction:: apilib.get_location_by_ll

下载 url 对应的 MP3 资源
------------------------
.. autofunction:: apilib.down_mp3_by_url

百度音乐 API
------------------------
.. autofunction:: apilib.music_baidu
