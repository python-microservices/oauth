# -*- coding: utf-8 -*-
# Copyright (c) 2018 by Alberto Vara <a.vara.1986@gmail.com>
import codecs
import os

from setuptools import setup, find_packages

version = __import__('project').__version__
author = __import__('project').__author__
author_email = __import__('project').__email__

if os.path.exists('README.rst'):
    long_description = codecs.open('README.rst', 'r', 'utf-8').read()
else:
    long_description = 'https://github.com/python-microservices/oauth'

setup(
    name="Oauth MS",
    version=version,
    author=author,
    author_email=author_email,
    description="Oauth Python Miscroservice",
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6"
    ],
    license="GPL",
    platforms=["any"],
    keywords="python, microservices",
    url='https://github.com/python-microservices/oauth',
    packages=find_packages(),
    zip_safe=True,
)