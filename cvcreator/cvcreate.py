#!/usr/bin/env python
# encoding: utf-8
# PYTHON_ARGCOMPLETE_OK

import argparse
import shutil
from glob import glob
import cvcreator as cv

def main():

    parser = argparse.ArgumentParser(
        description="A template based CV creater using YAML templates.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "filename", type=str, nargs="?",
        help="YAML source file.").completer = lambda prefix, **kws: glob("*.yaml")
    group.add_argument(
        "-y", "--yaml", action="store_true",
        help="Create simple YAML example.")

    parser.add_argument(
        "-t", "--template", type=str, dest="template",
        help="Select which template to use.").completer = (
            lambda prefix, **kws: cv.get_template_names())
    parser.add_argument(
        "-o", "--output", type=str, dest="output",
        help="Name of the output file.").completer = lambda prefix, **kws: glob("*.pdf")
    parser.add_argument(
        "-l", '--latex', action="store_true",
        help="Create latex file instead of pdf.")
    parser.add_argument(
        "-s", '--silent', action="store_true",
        help="Muffle output.")
    parser.add_argument(
        "a", metavar="a", type=int, nargs="*",
        help="Projects to include. Omit/0 for all/none.")

    parser.add_argument(
        "-lw", "--logo-width", type=str, dest="logo_width",
        help="Set the logo width.")
    parser.add_argument(
        "-lt", "--logo-top", type=str, dest="logo_top",
        help="Set the logo top position.")
    parser.add_argument(
        "-ll", "--logo-left", type=str, dest="logo_left",
        help="Set the logo left position.")
    parser.add_argument(
        "-lm", "--logo-margin", type=str, dest="logo_margin",
        help="Set the margin after logo.")

    args = parser.parse_args()

    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except:
        pass

    if args.yaml:
        yamlfile = cv.get_yaml_example()
        shutil.copy(yamlfile, "./example.yaml")
    else:
        with cv.cvopen(args.filename, template=args.template,
                       target=args.output) as src:

            config = src.get_config()

            if args.logo_width:
                config["logo_width"] = args.logo_width
            if args.logo_top:
                config["logo_top"] = args.logo_top
            if args.logo_left:
                config["logo_left"] = args.logo_left
            if args.logo_margin:
                config["logo_margin"] = args.logo_margin

            content = src.get_content()
            content.update(config)

            template = src.get_template()

            if 0 in args.a:
                content.pop("Projects", None)
            elif "Projects" not in content or not args.a:
                pass
            else:
                proj = content.pop("Projects", {})
                content["Projects"] = {}
                i = 1
                for n in args.a:
                    an = "A%d" % n
                    ai = "A%d" % i
                    if an in proj:
                        content["Projects"][ai] = proj.pop(an)
                    i += 1

            textxt = cv.parse(content, template)

            if args.latex:
                with open(args.filename[:-4]+"tex", "w") as f:
                    f.write(textxt)

            else:
                pdffile = src.compile(textxt, args.silent)

                destination = args.output or "."
                shutil.copy(pdffile, destination)
