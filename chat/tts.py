#!/usr/bin/env python3
# -*- coding:utf8 -*-
# PEP 8 check with Pylint
"""tts

Local and online TTS. 离在线语音合成。

Available functions:
- All classes and functions: 所有类和函数
"""
import os
import uuid
import requests
import pygame.mixer as mixer
import win32com.client


class RequestError(Exception):
    """RequestError.
    """
    pass

class TTS():
    """Online TTS.
    在线语音合成。

    It support instantiated with customized audioplayer.
    支持自定义音频播放器。

    Public attributes:
    - audioplayer: Audio player. 音频播放器。
    - app_key: API key of TTS service。 TTS服务的注册ID。
    - secret_key: API key of TTS service。 TTS服务的注册ID对应的密钥。
    - url_tok_base: The url of get token。 获取口令的URL地址。
    - url_get_base: The url of get requests。 GET请求的URL地址。
    - url_post_base: The url of get requests。 POST请求的URL地址。
    - language: The language of send text。 发送文本的语言。
    """
    def __init__(self, audioplayer=None, tempdir="."):
        if audioplayer:
            self.audioplayer = audioplayer
        else:
            self.audioplayer = mixer
        self.audioplayer.init()
        self.app_key = "QrhsINLcc3Io6w048Ia8kcjS"
        self.secret_key = "e414b3ccb7d51fef12f297ffea9ec41d"
        self.url_tok_base = "https://openapi.baidu.com/oauth/2.0/token"
        self.url_get_base = "http://tsn.baidu.com/text2audio"
        self.url_post_base = "http://tsn.baidu.com/text2audio"
        self.access_token = self.get_token()
        self.mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
        self.language = 'zh'
        self.tempdir = tempdir if os.path.isdir(tempdir) else "."

    def get_token(self):
        """Get token.
        获取API服务口令。
        """
        data = {
	            "grant_type": "client_credentials",
	            "client_id": self.app_key,
	            "client_secret": self.secret_key
	            }
        response = requests.get(url=self.url_tok_base, params=data)
        access_token = response.json()['access_token']
        return access_token

    def say(self, info):
        """Baidu TTS service.
        百度TTS服务。

        Official documents: http://yuyin.baidu.com/docs/tts/136
        """
        assert isinstance(info, str), "Info must be a string!"
        data = {
	            "tex": info,
	            "lan": self.language,
	            "vol": "9",
	            "cuid": self.mac_address,
	            "ctp": "1",
	            "tok": self.access_token
	            }
        headers = {"Content-Type": "audio/mp3"}
        try:
            response = requests.get(url=self.url_get_base, params=data, headers=headers)
            filename = self.tempdir + "/temp.mp3"
            with open(filename, "wb") as file:
                file.write(response.content)
            self.audioplayer.music.load(filename)
            self.audioplayer.music.play()
        except RequestError as error:
            print(error)


class LTTS():
    """Local TTS.
    离线语音合成。

    Based on Microsoft SAPI.
    基于微软SAPI。
    """
    def __init__(self, service=None):
        if service:
            self.service = service
        else:
            self.service = win32com.client.Dispatch("SAPI.SpVoice")
        self.language = 'zh'

    def say(self, info):
        """Say info.
        说出给定的信息。
        """
        self.service.Speak(info)
