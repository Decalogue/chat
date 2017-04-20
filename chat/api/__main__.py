#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Api lib for simple life."""
import sys
sys.path.append("../")
import api

while True:
    question = input('>')
    print(api.tuling(question))
    print(api.scene(question))
