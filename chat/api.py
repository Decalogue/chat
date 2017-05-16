#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Api lib for simple life."""
import os
import json
import requests
import time
import uuid
from urllib.request import urlopen

mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]

def nlu_tuling(question, loc="上海"):
    url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': "fd2a2710a7e01001f97dc3a663603fa1",
        'info': question,
        "loc": loc,
        'userid': mac_address
    }
    try:
        r = json.loads(requests.post(url=url, data=data).text)
    except:
        return
    if not r['code'] in (100000, 200000, 302000, 308000, 313000, 314000): return
    if r['code'] == 100000: # 文本类
        return '\n'.join([r['text'].replace('<br>','\n')])
    elif r['code'] == 200000: # 链接类
        return '\n'.join([r['text'].replace('<br>','\n'), r['url']])
    elif r['code'] == 302000: # 新闻类
        l = [r['text'].replace('<br>','\n')]
        for n in r['list']: l.append('%s - %s'%(n['article'], n['detailurl']))
        return '\n'.join(l)
    elif r['code'] == 308000: # 菜谱类
        l = [r['text'].replace('<br>','\n')]
        for n in r['list']: l.append('%s - %s'%(n['name'], n['detailurl']))
        return '\n'.join(l)
    elif r['code'] == 313000: # 儿歌类
        return '\n'.join([r['text'].replace('<br>','\n')])
    elif r['code'] == 314000: # 诗词类
        return '\n'.join([r['text'].replace('<br>','\n')])

def get_location_by_ip(city="上海市"): 
    url = "http://api.map.baidu.com/location/ip"
    data = {
        "ak": "wllxHD5CmWv8qX6CN2lyY73a",
        "coor": "bd09ll"
    }
    try:
        result = requests.post(url, data, timeout=20).text
        location = json.loads(result)["content"]["address"]
        print("网络正常，当前所在城市：", location)
    except:
        location = city
        print("网络异常，采用默认城市：", location)
    return location

def get_ll_by_address(address="", city="北京市"): 
    url = "http://api.map.baidu.com/geocoder/v2/"
    data = {
        "ak": "wllxHD5CmWv8qX6CN2lyY73a",
        "ret_coordtype": "gcj02ll", # bd09mc 百度米制坐标
        "address": address,
        # "city": city,
        "output": "json",
        "callback": "showLocation"
    }
    result = requests.post(url, data, timeout=20).text
    location = json.loads(result)
    return location

def get_location_by_ll(lat=39.908832488104686, lng=116.39753319791058): 
    url = "http://api.map.baidu.com/geocoder/v2/"
    data = {
        "ak": "wllxHD5CmWv8qX6CN2lyY73a",
        "coordtype": "bd09ll",
        "output": "json",
        "location": str(lat) + "," + str(lng),
        "pois": 0,
        "radius": 1000,
        #"callback": "renderReverse"
    }
    result = requests.post(url, data, timeout=20).text
    location = json.loads(result)
    return location

def down_mp3_by_url(song_url, song_name, song_size):
    file_name = song_name + ".mp3"
    base_dir = os.path.dirname(__file__)
    file_full_path = os.path.join(base_dir, file_name)  
    if os.path.exists(file_full_path):  
        return
    print("Begin downLoad %s, size = %d" % (song_name, song_size))  
    mp3 = urlopen(song_url)
    block_size = 8192
    down_loaded_size = 0
    file = open(file_full_path, "wb")  
    while True:  
        try:  
            buffer = mp3.read(block_size)             
            down_loaded_size += len(buffer)
            if(len(buffer) == 0):
                if down_loaded_size < song_size:
                    if os.path.exists(file_full_path):
                        os.remove(file_full_path)
                        print('download time out, file deleted')
                        with open('log.txt', 'a') as log_file:
                            log_file.write("time out rm %s\n" % file_name)
                break
            #print('%s %d of %d' % (song_name, down_loaded_size, song_size))  
            file.write(buffer)  
            if down_loaded_size >= song_size:  
                print('%s download finshed' % file_full_path)  
                break
        except:  
            if os.path.getsize(file_full_path) < song_size:  
                if os.path.exists(file_full_path):  
                    os.remove(file_full_path)  
                    print('download time out, file deleted')  
                    with open('log.txt', 'a') as log_file:  
                        log_file.write("time out rm %s\n" % file_name)  
            break
    file.close()  
    
def music_baidu(song="", singer=""):
    url = "http://tingapi.ting.baidu.com/v1/restserver/ting"
    current_time = time.time()
    # 获取榜单专辑
    # data_billboard_billList = {
        # "size": 10,
        # "type": 2,
        # "offset":0,
        # "callback": "",
        # "_t": current_time,
        # "format": "json",
        # "method": "baidu.ting.billboard.billList"
    # }
    # 查询歌曲
    data_search_catalogSug = {
        "query": song,
        "callback": "",
        "_t": current_time,
        "format": "json",
        "method": "baidu.ting.search.catalogSug"
    }
    # 播放歌曲
    data_song_play = {
        "songid": None, # 例如526109683代表(song="千年之约", singer="韩红")
        "callback": "",
        "_t": current_time,
        "format": "json",
        "method": "baidu.ting.song.play"
    }
    try:
        # 根据歌名查询歌曲
        result = json.loads(requests.post(url, data=data_search_catalogSug).text)
        # 根据歌手获取songid
        for item in result["song"]:
            if item["artistname"] == singer:
                data_song_play["songid"] = item["songid"]
                break
        if not data_song_play["songid"]:
            data_song_play["songid"] = result["song"][0]["songid"]
        # 根据songid查询资源
        result = json.loads(requests.post(url, data=data_song_play).text)
        send = {
            "islocal": 0,
            "author": result["songinfo"]["author"],
            "title": result["songinfo"]["title"],
            "lrc": result["songinfo"]["lrclink"],
            "pic_big": result["songinfo"]["pic_big"],
            "pic_premium": result["songinfo"]["pic_premium"],
            "url": result["bitrate"]["file_link"],
            "file_duration": result["bitrate"]["file_duration"],
            "file_size": result["bitrate"]["file_size"]
            }
    except:
        return ""
    return send
