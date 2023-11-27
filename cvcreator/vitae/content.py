import os
from typing import Any, List, Sequence

import toml
from .schema import VitaeContent, NorwegianVitaeContent
from .schema import TechnicalSkill
from .tech_skills import make_skill_groups, get_skills_data

CURDIR = f"{os.path.dirname(__file__)}{os.path.sep}"


def filter_(keys: str, sequence: Sequence[Any]) -> List[Any]:
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
        return list(sequence)
    keys = keys.replace(" ", "").split(",")
    return [sequence[idx] for idx, s in enumerate(sequence) if s.tag in keys]


def load_vitae(
    path: str,
    badges: bool = False,
    norwegian: bool = False,
    projects: str = "",
    publications: str = "",
) -> VitaeContent:
    """
    Load TOML content from disk.

    Also filters projects and publication lists, inserts icon prefixes to
    technical skills, and inserts default images as needed.

    Args:
        path:
            Path to the content to load.
        badges:
            Include small badge icons to selected technical skills.
        norwegian:
            If titles should be in Norwegian.
        projects:
            Comma-separated list of project tags to include. ':' includes all.
        publications:
            Comma-separated list of publication tags to include. ':' includes all.

    Returns:
        Loaded content as a nested data structure.

    """
    assert str(path).endswith(".toml"), (
        "must be TOML files with .toml extension.")
    with open(path) as src:
        if norwegian:
            content = NorwegianVitaeContent(**toml.load(src))
        else:
            content = VitaeContent(**toml.load(src))

    # filter projects and publications (as this can not be done in template)
    content.project = filter_(projects, content.project)
    content.publication = filter_(publications, content.publication)

    # remove potential duplicates from technical skills
    content.technical_skill = list(set(content.technical_skill))

    # place technical skills into groups
    content.technical_skill = make_skill_groups(content.technical_skill)

    if norwegian:
        norwegian_labels = get_skills_data()["norwegian_labels"]
        norwegian_skills = []
        for skill in content.technical_skill:
            norwegian_skills.append(TechnicalSkill(title=norwegian_labels[skill.title], values=skill.values))
        
        content.technical_skill = norwegian_skills

    if badges:
        for skill in content.technical_skill:
            for idx, value in enumerate(skill.values):
                path = os.path.join(
                    CURDIR, os.path.pardir, "data", "badges", f"{value}.pdf")
                if os.path.isfile(path):
                    skill.values[idx] = (
                        rf"\includegraphics[width=0.3cm]{{{path}}}~{value}")

    # anything with meta.*_image should be an image
    for name in content.meta.__dict__:
        if not name.endswith("_image"):
            continue
        value = getattr(content.meta, name)
        if not os.path.isfile(value):
            setattr(content.meta, name, os.path.join(
                CURDIR, os.path.pardir, "templates", f"{value}.pdf"))
            assert os.path.isfile(getattr(content.meta, name)), (
                f"unrecognized value/path for meta.{name}: '{value}'")

    return content
