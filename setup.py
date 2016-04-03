#!/usr/bin/env python
# encoding: utf8
# PYTHON_ARGCOMPLETE_OK

try:
    import autosudo # redo command with sudo, if failed
    import setup_completion # use setup.py argcomplete
except:
    pass

import shutil

from distutils.core import setup

shutil.copy("logo.pdf", "cvcreator/templates")
shutil.copy("config.yaml", "cvcreator/templates")

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
