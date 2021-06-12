"""Load latex template engine."""
import os
import glob

from jinja2 import Template

CURDIR = f"{os.path.dirname(__file__)}{os.path.sep}"
TEMPLATES = [os.path.basename(path).replace(".tex", "")
             for path in glob.glob(os.path.join(CURDIR, "templates", "*.tex"))]


def load_template(template_name: str) -> Template:
    """
    Load latex template from disk.

    Template is assumed to be latex code with extra Jinja2 commands:
    `\BLOCK{...}` and `\VAR{...}` for Jinja2 code block and variable insertion.

    Args:
        template_name:
            Either name of a available template, or path to a user provided
            template.

    Returns:
        Template engine for the given template with latex groups.

    """
    template = (os.path.join(CURDIR, "templates", f"{template_name}.tex")
                if template_name in TEMPLATES else template_name)
    assert os.path.isfile(template), (
        f"template '{template}' not valid path")

    with open(template, "r") as src:
        return Template(
            src.read(),
            block_start_string="\\BLOCK{",
            block_end_string="}",
            variable_start_string="\\VAR{",
            variable_end_string="}",
        )
