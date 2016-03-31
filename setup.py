#!/usr/bin/env python
# encoding: utf8

import sys
import shutil

from distutils.core import setup

shutil.copy("logo.pdf", "cvcreator/templates")

setup(
    name='cvcreator',
    version='0.4',
    scripts=["cvcreate"],
    packages=['cvcreator'],
    package_data={"cvcreator": ["templates/*"]},
    url='http://github.com/ExpertAnalytics/cvcreator',
    author="Jonathan Feinberg",
    author_email="jonathan@xal.no",
)
