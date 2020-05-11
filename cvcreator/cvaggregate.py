#!/usr/bin/env python
# encoding: utf-8
# PYTHON_ARGCOMPLETE_OK

import argparse
import shutil, os
import yaml
from glob import glob
import cvcreator as cv
from cvcreator import merge

MAX_NUM_CONST = 100

def tuple_of_ints(string):
    if string == "all":
        return tuple(range(1, MAX_NUM_CONST))
    else:
        return tuple(int(val) for val in string.split(","))

def main():
    parser = argparse.ArgumentParser(
        description="A template based CV creater using YAML templates.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "filename", type=str, nargs="?",
        help="YAML source file for company profile. Try ./examples/xal_agg.yaml").completer = lambda prefix, **kws: glob("*.yaml")
    group.add_argument(
        "-y", "--yaml", action="store_true",
        help="Create simple YAML example.")
    parser.add_argument(
        "-t", "--template", type=str, dest="template", default="aggregated",
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
        "-p", "--projects", type=tuple_of_ints, 
        default=(), help="Projects to include. Specify which entries by index or use 'all' to include all entries")
    parser.add_argument(
        "-u", "--publications", type=tuple_of_ints, 
        default=(), help="Publications to include. Specify which entris by integers or use all to inclue all entries.")
    parser.add_argument(
        "-a", "--aggregated", type=str, nargs="+",
        help="Collection of personal CVs to be aggregated. Try ./test/cv_repo/*.yaml")
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

    #Do we really want this for aggregation?
    if args.yaml:
        yamlfile = cv.get_yaml_example()
        shutil.copy(yamlfile, "./example.yaml")

    elif args.aggregated:
        joint_content = []
        
        #Add input from company profile as first entry in joint_content
        with open(args.filename) as src:
            joint_content.append(yaml.safe_load(src))
            
        #Add input from personal profiles successively
        for filename in args.aggregated:
            with open(filename) as src:
                joint_content.append(yaml.safe_load(src))

        #Merge the content in a new Dict
        merged_content = merge.merge_configurations(joint_content)

        #Define filename for temporary storage of merged content.
        merged_file = args.filename[:-5]+"_merged.yaml"

        #Write the merged content to file
        with open(merged_file, "w") as f:
            yaml.dump(merged_content,f,default_flow_style=False)            
        
        #Initialize workspace with merged content.
        with cv.cvopen(merged_file, template=args.template,
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

            if not args.projects:
                content.pop("Projects", None)
            else:
                proj = content.pop("Projects", {})
                content["Projects"] = {}
                for i, pn in enumerate(sorted(proj)):
                    n = int(pn[1:])
                    assert n < MAX_NUM_CONST, "Does not support cases for indices larger than MAX_NUM_CONST"
                    pi = "A%d" % i
                    if n in args.projects:
                        content["Projects"][pi] = proj.pop(pn)
            
            if not args.publications:
                content.pop("Publications", None)
            else:
                pub = content.pop("Publications", {})
                content["Publications"] = {}
                for i, un in enumerate(sorted(pub)):
                    n = int(un[1:])
                    assert n < MAX_NUM_CONST, "Does not support cases for indices larger than MAX_NUM_CONST"
                    ui = "B%d" % i
                    if n in args.publications:
                        content["Publications"][ui] = pub.pop(un)

            textxt = cv.parse(content, template)

            if args.latex:
                with open(args.filename[:-4]+"tex", "w") as f:
                    f.write(textxt)

            else:
                pdffile = src.compile(textxt, args.silent)

                #destination = args.output or "."
                destination = args.output or os.path.basename(args.filename)[:-5]+"_merged.pdf"#Remove path from filename and store in current folder
                shutil.copy(pdffile, destination)

            
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
            
            if not args.projects:
                content.pop("Projects", None)
            else:
                proj = content.pop("Projects", {})
                content["Projects"] = {}
                for i, pn in enumerate(sorted(proj)):
                    n = int(pn[1:])
                    assert n < MAX_NUM_CONST, "Does not support cases for indices larger than MAX_NUM_CONST"
                    pi = "A%d" % i
                    if n in args.projects:
                        content["Projects"][pi] = proj.pop(pn)
            
            if not args.publications:
                content.pop("Publications", None)
            else:
                pub = content.pop("Publications", {})
                content["Publications"] = {}
                for i, un in enumerate(sorted(pub)):
                    n = int(un[1:])
                    assert n < MAX_NUM_CONST, "Does not support cases for indices larger than MAX_NUM_CONST"
                    ui = "B%d" % i
                    if n in args.publications:
                        content["Publications"][ui] = pub.pop(un)
            
            textxt = cv.parse(content, template)

            if args.latex:
                with open(args.filename[:-4]+"tex", "w") as f:
                    f.write(textxt)

            else:
                pdffile = src.compile(textxt, args.silent)

                destination = args.output or "."
                shutil.copy(pdffile, destination)
