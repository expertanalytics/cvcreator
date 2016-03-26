#!/usr/bin/env python
# encoding: utf8

import sys
import shutil

from distutils.core import setup

shutil.copy("logo.pdf", "cvcreator/templates")

setup(
    name='cvcreator',
    version='0.4',
    packages=['cvcreator'],
    package_data={"cvcreator": ["templates/*"]},
    url='http://github.com/ExpertAnalytics/cvcreator',
    author="Jonathan Feinberg",
    author_email="jonathan@xal.no",
)

if sys.version_info.major == 2:
    input = raw_input
    src = "cvcreate2.py"
else:
    src = "cvcreate3.py"


def copy_script():

    query = input("[y]es/[n]o/[c]ustom location:")
    query = query[:1].lower()

    if query == "y":
        target = "/usr/local/bin/cvcreate"
        shutil.copy(src, target)

    elif query == "n":
        sys.exit(0)

    elif query == "c":
        target = input("Input path:")
        shutil.copy(src, target)

    else:
        print("please select valid option")
        copy_script()


print("Copy cvcreate script to /usr/local/bin?")
copy_script()
