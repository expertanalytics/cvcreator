"""Command line interface parser."""
import os
import shutil
import glob

import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand

from .compile import compile_latex
from .content import load_content
from .template import load_template
from .txt2yaml import convert_txt_to_yaml
from .yaml2toml import convert_yaml_to_toml


@click.group(
    cls=HelpColorsGroup,
    help_headers_color="green",
    help_options_color="blue",
    short_help="CV creator tool",
)
def cv():
    """
    Command line tool for creating curriculum vitae from TOML source files.
    """
    pass


@cv.command(
    cls=HelpColorsCommand,
    help_options_color="blue",
    short_help="Create CV as .pdf file",
)
@click.argument("toml_content")
@click.argument("document_output", default="")
@click.option("-t", "--template", default="default", help=(
    "Select which latex template file to use when generating document."))
@click.option("-p", "--projects", default="", help=(
    "Comma-separated list of project tags to include. Use ':' for all."))
@click.option("-u", "--publications", default="", help=(
    "Comma-separated list of publication tags to include. Use ':' for all."))
def create(
    toml_content: str,
    document_output: str = "",
    template: str = "default",
    projects: str = "",
    publications: str = "",
) -> None:
    """
    Create curriculum vitae .pdf document from .toml content file.
    """
    content = load_content(toml_content, projects, publications)
    template = load_template(template)
    latex_code = template.render(**dict(content))
    name = os.path.basename(toml_content.replace(".toml", ""))
    document_output = document_output or toml_content.replace(".toml", ".pdf")
    with compile_latex(latex=latex_code, name=name) as pdf_path:
        shutil.copy(pdf_path, document_output)


@cv.command(cls=HelpColorsCommand, short_help="Create CV as .tex file")
@click.argument("toml_content")
@click.argument("target", default="")
@click.option("-t", "--template", default="default", help=(
    "Select which latex template file to use when generating document."))
@click.option("-p", "--projects", default="", help=(
    "Comma-separated list of project tags to include. Use ':' for all."))
@click.option("-u", "--publications", default="", help=(
    "Comma-separated list of publication tags to include. Use ':' for all."))
def latex(
    toml_content: str,
    target: str = "",
    template: str = "default",
    projects: str = "",
    publications: str = "",
):
    """
    Create latex source code from .toml content file.
    """
    content = load_content(toml_content, projects, publications)
    template = load_template(template)
    latex_code = template.render(**dict(content))
    target = target or toml_content.replace(".toml", ".tex")
    with open(target, "w") as dst:
        dst.write(latex_code)


@cv.command(cls=HelpColorsCommand, short_help="Convert old .txt to .yaml")
@click.argument("txt_source")
@click.argument("yaml_target", default="")
def txt2yaml(txt_source, yaml_target):
    """
    Convert old .txt content file into newer(-ish) .yaml format.
    """
    convert_txt_to_yaml(txt_source, yaml_target)


@cv.command(cls=HelpColorsCommand, short_help="Convert old .yaml to .toml")
@click.argument("yaml_source")
@click.argument("toml_target", default="")
def yaml2toml(yaml_source, toml_target):
    """
    Convert old .yaml content file into newer .toml format.
    """
    convert_yaml_to_toml(yaml_source, toml_target)


@cv.command(cls=HelpColorsCommand, short_help="Create example .toml file")
@click.argument("toml_target")
def example(toml_target):
    """
    Create example .toml content file to be filled out.
    """
    toml_source = os.path.join(os.path.dirname(__file__), "templates", "example.toml")
    shutil.copy(toml_source, toml_target)


@cv.command(cls=HelpColorsCommand, short_help="List technical skill badges")
def badges():
    r"""
    List the technical skills that will trigger a badge prefix.
    In other words, the text will be accompanied with an appropriate logo image.

    Notable exemption: 'Latex' though it has a logo, should be preferred to be
    included as '\\LaTeX' as the actual logo is usually unrecognizable.
    """
    os.chdir(os.path.join(os.path.dirname(__file__), "icons"))
    click.echo_via_pager("\n".join(badge.replace(".pdf", "")
                                   for badge in sorted(glob.iglob("*.pdf"))))
