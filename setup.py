#!/usr/bin/env python
# encoding: utf8
# PYTHON_ARGCOMPLETE_OK

import sys
import os
import shutil
from setuptools import setup

shutil.copy("logo.pdf", "cvcreator/templates")
shutil.copy("footer.pdf", "cvcreator/templates")
shutil.copy("config.yaml", "cvcreator/templates")

setup(
    name="cvcreator",
    version="0.4.9",
    url="http://github.com/ExpertAnalytics/cvcreator",

    author="Jonathan Feinberg",
    author_email="jonathan@xal.no",

    packages=["cvcreator"],
    package_data={"cvcreator": ["templates/*"]},
    entry_points={
        "console_scripts": [
            "cvcreate = cvcreator.cvcreate:main",
            "txt2yaml = cvcreator.txt2yaml:main",
        ]
    },
    install_requires=[
        "pyyaml",
    ],
    zip_safe=False,
)

if "develop" not in sys.argv:
    os.remove("cvcreator/templates/logo.pdf")
    os.remove("cvcreator/templates/footer.pdf")
    os.remove("cvcreator/templates/config.yaml")
