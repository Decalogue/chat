#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

import sys
if sys.version_info < (3, 3):
    print("THIS MODULE REQUIRES PYTHON 3.3+. YOU ARE CURRENTLY USING PYTHON {0}".format(sys.version))
    sys.exit(1)

import chat

setup(
    name = "chat",
    version = chat.__version__,
    packages = ["chat"],
    include_package_data = True,

    # PyPI metadata
    author = chat.__author__,
    author_email = "1044908508@qq.com",
    description = chat.__doc__,
    long_description = open("README.rst").read(),
    license = chat.__license__,
    keywords = "chat NLP MachineLearning",
    url = "https://github.com/decalogue/chat",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
		"Natural Language :: Chinese",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Other OS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: MachineLearning :: NLP :: ChatRobot",
    ],
)
