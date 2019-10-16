# encoding: utf-8
"""
"""

import glob
import inspect
import os
import shutil
import tempfile
import yaml
import subprocess

import cvcreator

__all__ = ["cvopen", "get_template_names", "get_yaml_example"]


def get_template_names():
    """Get available template names
    Faster then creating a full Workspace and retriving it from there.
    """
    templatedir = os.path.dirname(inspect.getfile(cvcreator))
    templatedir = templatedir + os.path.sep + "templates" + os.path.sep
    templates = glob.glob(templatedir + "*.yaml")
    templates = [os.path.basename(t)[:-5] for t in templates]
    if "config" in templates:
        templates.remove("config")
    return templates


def get_yaml_example():
    """Get YAML example filename."""
    templatedir = os.path.dirname(inspect.getfile(cvcreator))
    templatedir = templatedir + os.path.sep + "templates" + os.path.sep
    yamlfile = templatedir + "example"
    return yamlfile


class cvopen(object):

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

        with open(filename, "r") as f:
            content = f.read()

        content = content \
            .replace("æ", r"{\ae}") \
            .replace("Æ", r"{\AE}") \
            .replace("ø", r"{\o}") \
            .replace("Ø", r"{\O}") \
            .replace("å", r"{\aa}") \
            .replace("Å", r"{\AA}") \
            .replace("é", r"{\'e}") \
            .replace("É", r"{\'E}")

        with open(self.path + "_content", "w") as f:
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
        raise ValueError(
            "Template '%s' not found in available templates: %s" % (
                template, get_template_names()))

    def get_template(self, template=None):

        if not template:
            template = self.template

        if not os.path.isfile(self.path + template + ".yaml"):
            self.template_not_found(template)

        with open(self.path + template + ".yaml") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)

    def get_content(self):
        with open(self.path + "_content") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)

    def get_config(self):
        with open(self.path + "config.yaml") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)

    def compile(self, textxt, silent):

        texname = self.target[:-3] + "tex"
        with open(self.path + texname, "w") as f:
            f.write(textxt)

        #print("wrote %s" % (self.path + texname))
        if silent:
            silentstr = "-silent"
        else:
            silentstr = ""
        if os.name == 'nt':
            separator = "&" #Windows systems use & instead of ; in shell
        else:
            separator = ";"
        cmd = ("cd \"%s\" %s latexmk \"%s\" %s -pdf "
                "-latexoption=\"-interaction=nonstopmode\""
                % (self.path, separator, texname, silentstr))
        p = subprocess.Popen(cmd, shell=True)
        p.wait()
        if (p.returncode): #Non-zero return code from call to latexmk
            print("latexmk run failed, see errors above ^^^")
            print("trying pdflatex instead...")
            cmd = (" %s pdflatex \"%s\" %s "
                    "-latexoption=\"-interaction=nonstopmode\""
                    % (separator, texname, silentstr))
            cmd = ("cd \"%s\"" % (self.path)) + cmd + cmd
            p = subprocess.Popen(cmd, shell=True)
            p.wait()
            if (p.returncode): #Non-zero return code from call to pdflatex
                print("pdflatex run failed too, see errors above ^^^")
        pdfname = self.path + self.target
        assert os.path.isfile(pdfname)
        return pdfname
