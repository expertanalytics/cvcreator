#!/usr/bin/env python
# encoding: utf8
# PYTHON_ARGCOMPLETE_OK

import shutil

from distutils.core import setup

shutil.copy("logo.pdf", "cvcreator/templates")
shutil.copy("footer.pdf", "cvcreator/templates")
shutil.copy("config.yaml", "cvcreator/templates")

setup(
    name='cvcreator',
    version='0.4.1',
    scripts=["cvcreate"],
    packages=['cvcreator'],
    package_data={"cvcreator": ["templates/*"]},
    url='http://github.com/ExpertAnalytics/cvcreator',
    author="Jonathan Feinberg",
    author_email="jonathan@xal.no",
)
