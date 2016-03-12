#!/usr/bin/env python
# encoding: utf8

import sys
import os
import glob
import shutil

from distutils.core import setup

os.chdir(os.path.dirname(sys.argv[0]))

shutil.copy("logo.pdf", "cvcreator/templates")

setup(
    name='cvcreator',
    version='0.4',
    packages=['cvcreator'],
    package_data = {"cvcreator": ["templates/*"]},
    url='http://github.com/ExpertAnalytics/cvcreator',
    author="Jonathan Feinberg",
    author_email="jonathan@xal.no",
)

if sys.version_info.major == 2:
    input = raw_input
    src = "frontend2.py"
else:
    src = "frontend3.py"

def copy_script():

    q = input("[y]es/[n]o/[c]ustom location:")
    q = q[:1].lower()

    if q == "y":
        target = "/usr/local/bin/cvcreate"

    elif q == "n":
        sys.exit(0)

    elif q == "c":
        target = input("Input path:")

    else:
        print("please select valid option")
        copy_script()

    shutil.copy(src, target)

print("Copy cvcreate script to /usr/local/bin?")
copy_script()
