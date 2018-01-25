# -*- coding:utf8 -*-

import os
from configparser import ConfigParser

def getConfig(section, key):
    config = ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/conf/self.conf'
    config.read(path, encoding='UTF-8')
    return config.get(section, key)
