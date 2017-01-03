"""
cvparser library
----------------

A library for automated create CV on the fly.
"""
import shutil

from cvcreator.parser import parse
from cvcreator.workspace import cvopen, get_yaml_example

__all__ = ["main"]


def main(args):

    if args.yaml:

        yamlfile = get_yaml_example()
        shutil.copy(yamlfile, "./example.yaml")

    else:

        with cvopen(args.filename, template=args.template,
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

            textxt = parse(content, template)

            if args.latex:
                with open(args.filename[:-4]+"tex", "w") as f:
                    f.write(textxt)

            else:
                pdffile = src.compile(textxt, args.silent)

                destination = args.output or "."
                shutil.copy(pdffile, destination)
