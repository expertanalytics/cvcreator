"""Test configuration file."""
import os
import glob
from distutils.dir_util import copy_tree, remove_tree  # pylint: disable=no-name-in-module,import-error

import yaml
import pytest


@pytest.fixture(scope="function", autouse=True)
def workspace(tmpdir_factory):
    """
    Create a temporary workspace folder to work from during tests.

    Content placed in ``test/data`` will be available.
    """
    tmp_folder = str(tmpdir_factory.mktemp("workspace"))

    source_folder = str(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test", "data"))
    copy_tree(source_folder, tmp_folder, verbose=0)

    cur_folder = os.path.abspath(os.path.curdir)
    os.chdir(tmp_folder)
    yield tmp_folder
    os.chdir(cur_folder)

    remove_tree(tmp_folder, verbose=0)


@pytest.fixture(scope="function")
def person1(workspace):
    with open(f"{workspace}/person1.yaml") as src:
        yield yaml.safe_load(src)


@pytest.fixture(scope="function")
def person2(workspace):
    with open(f"{workspace}/person2.yaml") as src:
        yield yaml.safe_load(src)
