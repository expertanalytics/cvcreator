# encoding: utf-8
"""
"""
import tempfile
import shutil
import inspect
import glob
import os
import yaml

import cvcreator

__all__ = ["open", "get_template_names", "get_yaml_example"]

builtin_open = open # because override


def get_template_names():
    """
Get available template names

Faster then creating a full Workspace and retriving it from there.
    """
    templatedir = os.path.dirname(inspect.getfile(cvcreator))
    templatedir = templatedir + os.path.sep + "templates" + os.path.sep
    templates = glob.glob(templatedir + "*.yaml")
    templates = [os.path.basename(t)[:-5] for t in templates]
    return templates

def get_yaml_example():
    """
Get YAML example filename
    """
    templatedir = os.path.dirname(inspect.getfile(cvcreator))
    templatedir = templatedir + os.path.sep + "templates" + os.path.sep
    yamlfile = templatedir + "example"
    return yamlfile


class open(object):

    def __init__(self, filename, template=None, target=None):

        assert os.path.isfile(filename)
        self.path = tempfile.mkdtemp() + os.path.sep

        self.filename = os.path.basename(filename)
        if target:
            self.target = target
        else:
            self.target = os.path.basename(filename)[:-4] + "pdf"

        # get template dir
        templatedir = os.path.dirname(inspect.getfile(cvcreator))
        templatedir = templatedir + os.path.sep + "templates" + os.path.sep
        assert os.path.isdir(templatedir)

        # copy everything over
        for name in glob.glob(templatedir + "*"):
            shutil.copy(name, self.path)

        with builtin_open(filename, "r") as f:
            content = f.read()

        content = content.replace("æ", "\\ae{}"
                                  ).replace("Æ", "\\AE{}"
                                  ).replace("ø", "\\o{}"
                                  ).replace("Ø", "\\O{}"
                                  ).replace("å", "\\aa{}"
                                  ).replace("Å", "\\AA{}"
                                  ).replace("é", "\\'e{}"
                                  ).replace("É", "\\'E{}")

        with builtin_open(self.path + "_content", "w") as f:
            f.write(content)

        # process template name
        if not template:
            template = "default"
        template = template
        if not os.path.isfile(self.path + template + ".yaml"):
            self.template_not_found(template)
        self.template = template


    def __enter__(self):
        return self

    def __exit__(self, typ, val, traceb):
        self.close()

    def close(self):
        shutil.rmtree(self.path)

    def template_not_found(self, template):
        raise ValueError("""\
Template '%s' not found in available templates:
%s""" % (template, get_template_names()))

    def get_template(self, template=None):

        if not template:
            template = self.template

        if not os.path.isfile(self.path + template + ".yaml"):
            self.template_not_found(template)

        with builtin_open(self.path + template + ".yaml") as f:
            return yaml.load(f)


    def get_content(self):
        with builtin_open(self.path + "_content") as f:
            return yaml.load(f)

    def compile(self, textxt):

        texname = self.path + self.target[:-3] + "tex"
        with builtin_open(texname, "w") as f:
            f.write(textxt)

        os.system("cd %s; latexmk %s -pdf -latexoption=\"-interaction=nonstopmode\"" % (self.path, texname))

        pdfname = self.path + self.target
        assert os.path.isfile(pdfname)
        return pdfname



