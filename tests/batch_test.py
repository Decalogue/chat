#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PEP 8 check with Pylint
"""Batch test.
"""

import sys
sys.path.append("../")
from chat.client import batch_test

if __name__ == '__main__':
    batch_test("testcase.txt")
