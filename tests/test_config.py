#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PEP 8 check with Pylint
"""Config
"""
import sys
sys.path.append("../")
from chat.client import config

if __name__ == "__main__":
    config(info="", userid="A0001")
    config(info="基础命令 基础问答 基础银行 民生银行 客户问答", userid="A0001")