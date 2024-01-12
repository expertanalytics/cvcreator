"""Command line interface parser."""
from typing import List
import os
import re
import shutil
import glob

import toml
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand

from .compile import compile_latex
from .template import load_template

from .vitae import load_vitae
from .aggregate import load_aggregate
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


@cv.command(
    cls=HelpColorsCommand,
    help_options_color="blue",
    short_help="Create CV as .pdf file",
)
@click.argument("toml_content")
@click.argument("output", default="")
@click.option("-b", "--badges", is_flag=True, help=(
    "Include small badge icons to selected technical skills."))
@click.option("-l", "--latex", is_flag=True, help=(
    "Output latex document instead of a pdf."))
@click.option("-n", "--norwegian", is_flag=True, help=(
    "Generate titles in Norwegian."))
@click.option("-p", "--projects", default="", help=(
    "Comma-separated list of project tags to include. Use ':' for all."))
@click.option("-u", "--publications", default="", help=(
    "Comma-separated list of publication tags to include. Use ':' for all."))
@click.option("-", "--publications", default="", help=(
    "Comma-separated list of publication tags to include. Use ':' for all."))
def create(
    toml_content: str,
    output: str = "",
    badges: bool = False,
    latex: bool = False,
    norwegian: bool = False,
    projects: str = "",
    publications: str = "",
) -> None:
    """
    Create curriculum vitae from TOML content file.
    """
    content = load_vitae(toml_content, badges=badges, norwegian=norwegian,
                         projects=projects, publications=publications)
    template = load_template("vitae.tex")
    latex_code = template.render(**dict(content))
    if latex:
        output = output or toml_content.replace(".toml", ".tex")
        with open(output, "w") as dst:
            dst.write(latex_code)
    else:
        name = os.path.basename(toml_content.replace(".toml", ""))
        output = output or toml_content.replace(".toml", ".pdf")
        with compile_latex(latex=latex_code, name=name) as pdf_path:
            shutil.copy(pdf_path, output)


@cv.command(cls=HelpColorsCommand, short_help="Create aggregate CSV file")
@click.argument("agg_content")
@click.argument("cv_content", nargs=-1, required=True)
def aggregate(
    agg_content: str,
    cv_content: List[str],
):
    """
    Create aggregate .csv from series of .toml content files.
    """
    content = load_aggregate(agg_content, cv_content)
    template = load_template("aggregate.csv")
    csv_string = template.render(**dict(content))
    output = agg_content.replace(".toml", ".csv")
    with open(output, "w") as dst:
        dst.write(csv_string)


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


@cv.command(cls=HelpColorsCommand, short_help="Create example TOML file")
@click.argument("toml_target")
def example(toml_target):
    """
    Create example .toml content file to be filled out.
    """
    toml_source = os.path.join(os.path.dirname(__file__), "templates", "example.toml")
    shutil.copy(toml_source, toml_target)


@cv.command(cls=HelpColorsCommand, short_help="List allowed technical skills")
@click.option("--badges", is_flag=True, help=(
    "Only list skills that has an associated icon."))
def skills(badges):
    """
    List of allowed technical skills. The spelling is case sensitive.
    """
    if badges:
        icons = glob.glob(os.path.join(os.path.dirname(__file__), "data", "badges", "*.pdf"))
        data = (re.sub(r".*/([^/]+).pdf$", r"\1", icon) for icon in icons)
    else:
        path = os.path.join(os.path.dirname(__file__), "data", "tech_skills.toml")
        with open(path) as handle:
            data = toml.load(handle)["skills"]
    click.echo("\n".join(data))
