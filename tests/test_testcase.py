#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PEP 8 check with Pylint
"""Upload user data to graph from usb interface.
"""
import sys
sys.path.append("../")
from chat.testcase import generate_test_cases

if __name__ == '__main__':
    # generate_test_cases(filename="C:/nlu/data/chat.xls", custom_sheets=["基础命令", "基础问答"])
    generate_test_cases(filename="new.xls")