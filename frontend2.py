#!/usr/bin/env python
# encoding: utf-8
# PYTHON_ARGCOMPLETE_OK

import argparse
from textwrap import dedent
from glob import glob
import cvcreator as cv

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=dedent("""\
A template based CV creater using YAML templates.
"""))

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("filename", type=str, nargs="?",
        help="YAML source file.").completer=\
                lambda prefix, **kws: glob("*.yaml")

group.add_argument("-y", '--yaml', action="store_true",
        help="""Create simple YAML example.""")

parser.add_argument("-t", "--template", type=str, dest="template",
        help="Select which template to use.").completer=\
                lambda prefix, **kws: cv.get_template_names()

parser.add_argument("-o", "--output", type=str, dest="output",
        help="Name of the output file.").completer=\
                lambda prefix, **kws: glob("*.pdf")

parser.add_argument("-l", '--latex', action="store_true",
        help="""Create latex file instead of pdf.""")

parser.add_argument("a", metavar="a", type=int, nargs="*",
        help="Projects to include. Omit/0 for all/none.")


try:
    import argcomplete
    argcomplete.autocomplete(parser)
except:
    pass

if __name__ == "__main__":

    args = parser.parse_args()
    cv.main(args)

