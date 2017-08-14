#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from pydub import AudioSegment
from chat.mytools import Walk

# 选择ffmpeg路径
AudioSegment.converter = "C:/rain/software/ffmpeg/bin/ffmpeg"
# 选择待处理的音频目录
path = "C:\\rain\\cloud\\train\\data\\nlu\\audio\\merge"
# 获取所有子目录全路径
walker = Walk()
dirlist = walker.dir_process(1, path, style="dirlist")
# print(dirlist)
# 初始化音频列表
audio = []
# 对每个子目录下的音频文件分别进行合并
for dir in dirlist:
    # 获取文件列表
    newwalker = Walk()
    filelist = newwalker.dir_process(1, dir, style="filelist")
    # print(filelist)
    # 加载MP3文件
    for file in filelist:
        audio.append(AudioSegment.from_mp3(file))
    # 合并多个音频
    audio = sum(audio)
    # 导出合并音频
    audio.export(dir + ".mp3", format="mp3")
    # 重置
    audio = []
        
# 加载MP3文件
audio1 = AudioSegment.from_mp3("first.mp3")
audio2 = AudioSegment.from_mp3("second.mp3")

# 取得两个MP3文件的声音分贝
db1 = audio1.dBFS
db2 = audio2.dBFS

# audio1 = audio1[300:] # 从300ms开始截取MP3

# 调整两个MP3的声音大小，防止出现一个声音大一个声音小的情况
dbplus = db1 - db2
if dbplus < 0: # audio1的声音更小
    audio1 += abs(dbplus)
elif dbplus > 0: # audio2的声音更小
    audio2 += abs(dbplus)

#拼接两个音频文件
audio = audio1 + audio2

#导出音频文件
audio.export("result.mp3", format="mp3") #导出为MP3格式

if __name__ == '__main__':
    print("ok")
