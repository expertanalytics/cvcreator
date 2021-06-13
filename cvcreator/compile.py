from contextlib import contextmanager
import tempfile
import os
import sys
import subprocess

import click


@contextmanager
def compile_latex(
    latex: str,
    name: str = "document",
    silent: bool = False,
) -> None:
    """
    Compile latex code.

    Will try to use latexmk first, then pdflatex.
    Assumes that at least one of these executable exists in path.

    Args:
        latex:
            The latex source code as a string.
        name:
            The name of the file to be used during compilation.
            The extensions `.tex` and `.pdf` will be added.
        silent:
            Muffle latex compiles.

    """
    with tempfile.TemporaryDirectory() as folder:
        source_file = os.path.join(folder, f"{name}.tex")

        click.echo(f"writing {source_file}")
        with open(source_file, "w") as dst:
            dst.write(latex)

        sep = "&" if os.name == "nt" else ";"
        silent = "-silent" if silent else ""

        if not silent:
            click.secho(f"trying to compile {name}.tex", fg="yellow")
        proc = subprocess.Popen(
            f'cd "{folder}" {sep} latexmk {source_file} {silent} '
            '-pdf -latexoption="-interaction=nonstopmode"',
            shell=True,
        )
        proc.wait()
        if proc.returncode:
            click.secho("latexmk run failed, see errors above ^^^", fg="red")
            click.secho("trying pdflatex instead...", fg="yellow")
            proc = subprocess.Popen(
                f'cd "{folder}" {sep} pdflatex {source_file} '
                '{silent} -latexoption="-interaction=nonstopmode"',
                shell=True
            )
            proc.wait()
            if proc.returncode:
                click.secho("pdflatex run failed too, see errors above ^^^", fg="red")
                sys.exit(2)
        if not silent:
            click.secho(
                f"Document successfully compiled: {name}.tex -> {name}.pdf", fg="green")
        yield source_file.replace(".tex", ".pdf")
