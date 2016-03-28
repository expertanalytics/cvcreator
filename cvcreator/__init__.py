"""
cvparser library
----------------

A library for automated create CV on the fly.
"""
import shutil
import os
builtin_open = open # because override

import cvcreator.parser
from cvcreator.parser import *

import cvcreator.workspace
from cvcreator.workspace import *

def main(args):

    if args.yaml:

        yamlfile = get_yaml_example()
        shutil.copy(yamlfile, "./example.yaml")
    
    else:

        with cvcreator.open(args.filename, template=args.template,
                            target=args.output) as src:

            content = src.get_content()
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

            textxt = parse(content, template)

            if args.latex:
                with builtin_open(args.filename[:-4]+"tex", "w") as f:
                    f.write(textxt)

            else:
                pdffile = src.compile(textxt, args.silent)

                destination = args.output or "."
                shutil.copy(pdffile, destination)
