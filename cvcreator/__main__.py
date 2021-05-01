"""Main executable."""
from typing import Any, Sequence
import argparse
import shutil
import glob
import tempfile
import os
import subprocess

from jinja2 import Template

from .schema import VitaeContent

CURDIR = f"{os.path.dirname(__file__)}{os.path.sep}"
TEMPLATES = [os.path.basename(path).replace(".tex", "")
             for path in glob.glob(os.path.join(CURDIR, "templates", "*.tex"))]


def filter_(keys: str, sequence: Sequence[Any]) -> Sequence[Any]:
    """
    Filter a sequence form CLI.

    Args:
        keys:
            String with comma-separated tags. Or the string ':'.
        sequence:
            Sequence of elements to filter.

    Returns:
        Same as `sequence`, but filtered down to indices included in `keys`.

    """
    if keys == "":
        return []
    if keys == ":":
        return sequence
    keys = keys.replace(" ", "").split(",")
    return [sequence[idx] for idx, s in enumerate(sequence) if s.tag in keys]


def compile_(latex: str, source: str, output: str, silent: bool = True) -> None:
    """
    Compile latex code.

    Will try to use latexmk first, then pdflatex.
    Assumes that either of these executable exists.

    Args:
        latex:
            The latex source code.
        source:
            The name of the latex source files.
        output:
            The folder for where to store output PDF.
        silent:
            Muffle latex compiles.

    """
    with tempfile.TemporaryDirectory() as folder:

        source_name = os.path.basename(source)
        print(f"writing {folder}{os.path.sep}{source_name}")
        with open(f"{folder}{os.path.sep}{source_name}", "w") as dst:
            dst.write(latex)

        sep = "&" if os.name == "nt" else ";"
        silent = "-silent" if silent else ""
        cmd_args = '{silent} -latexoption="-interaction=nonstopmode"'

        print(f"compiling {folder}{os.path.sep}{source_name}")
        proc = subprocess.Popen(
            f'cd "{folder}" {sep} latexmk "{source_name}" {silent} '
             '-pdf -latexoption="-interaction=nonstopmode"',
            shell=True,
        )
        proc.wait()
        if proc.returncode:
            print("latexmk run failed, see errors above ^^^")
            print("trying pdflatex instead...")
            proc = subprocess.Popen(
                f'cd "{folder}" {sep} pdflatex "{source_name}" '
                 '{silent} -latexoption="-interaction=nonstopmode"',
                shell=True
            )
            proc.wait()
            if proc.returncode:
                print("pdflatex run failed too, see errors above ^^^")
                return

        source = source.replace(".tex", ".pdf")
        source_name = source_name.replace(".tex", ".pdf")
        print(f"moving {folder}{os.path.sep}{source_name} -> {output}")
        shutil.copy(f'{folder}{os.path.sep}{source_name}', output or source)


def make_parser() -> argparse.ArgumentParser:
    """Make an argument parser."""
    parser = argparse.ArgumentParser(
        description="A template based CV creater using YAML templates.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "source", type=str, nargs="?",
        help="yaml source file to read. (If omitted create example source file.)"
    ).completer = lambda prefix, **kws: glob.glob("*.yaml")
    parser.add_argument(
        "-t", "--template", type=str, default="default",
        help="Select which latex template to use when generating document."
    ).completer = lambda prefix, **kws: TEMPLATES
    parser.add_argument(
        "-o", "--output", type=str, default="",
        help="Name of the output file. Default to 'source' with pdf-extension",
    )
    parser.add_argument(
        "-l", '--latex', action="store_true",
        help="Create latex instead of pdf."
    )
    parser.add_argument(
        "-s", '--silent', action="store_true",
        help="Muffle output.")
    parser.add_argument(
        "-p", "--projects", type=str, default="",
        help="Comma-seperated list of project tags to include. Use ':' for all.")
    parser.add_argument(
        "-u", "--publications", type=str, default="",
        help="Comma-seperated list of publication tags to include. Use ':' for all.")
    parser.add_argument(
        "--font-size", type=int, default=11,
        help="The size of the font used in the document."
    )
    parser.add_argument(
        "--logo-image", type=str, default="logo",
        help="path to image files compatible with latexpdf."
    )
    parser.add_argument(
        "--footer-image", type=str, default="footer",
        help="path to image files compatible with latexpdf."
    )
    return parser


def main() -> None:
    """Execution script."""
    parser = make_parser()
    args = parser.parse_args()

    # no source, no problem: let's make one!
    if not args.source:
        with open(os.path.join(CURDIR, "templates", "example.yaml")) as src:
            with open(args.source or "example.yaml", "w") as dst:
                dst.write(src.read())
        return

    assert args.source.endswith(".yaml"), "must be YAML files with .yaml extension"
    content = VitaeContent.load(args.source)

    # filter projects and publications (as this can not be done in template)
    content.project = filter_(args.projects, content.project)
    content.publication = filter_(args.publications, content.publication)

    # verify paths to templates and images
    template = (os.path.join(CURDIR, "templates", f"{args.template}.tex")
                if args.template in TEMPLATES else args.template)
    assert os.path.isfile(template), (
        "template '%s' not valid path" % args.template)

    footer_image = (args.footer_image if os.path.isfile(args.footer_image)
                    else os.path.join(CURDIR, "templates",
                                      f"{args.footer_image}.pdf"))
    assert os.path.isfile(footer_image), (
        "footer_image '%s' not valid path" % args.footer_image)

    logo_image = (args.logo_image if os.path.isfile(args.logo_image)
                  else os.path.join(CURDIR, "templates",
                                    f"{args.logo_image}.pdf"))
    assert os.path.isfile(logo_image), (
        "logo_image '%s' not valid path" % args.logo_image)

    # Merge source and template:
    with open(template, "r") as src:
         template = Template(
            src.read(),
            block_start_string="\\BLOCK{",
            block_end_string="}",
            variable_start_string="\\VAR{",
            variable_end_string="}",
        )
    latex = template.render(
        logo_image=logo_image,
        footer_image=footer_image,
        font_size=args.font_size,
        **dict(content),
    )

    # (compile and) store results:
    if args.latex:
        output = args.output or args.source.replace(".yaml", ".tex")
        with open(output, "w") as dst:
            dst.write(latex)
    else:
        output = args.output or args.source.replace(".yaml", ".pdf")
        compile_(
            latex=latex,
            source=args.source.replace(".yaml", ".tex"),
            output=output,
            silent=args.silent,
        )
