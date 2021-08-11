import os
from typing import Dict, List
from collections import defaultdict

import toml

from ..vitae import load_vitae
from ..vitae.tech_skills import get_skills_data
from .schema import AggregateContent, SkillCount

CURDIR = f"{os.path.dirname(__file__)}{os.path.sep}"


def load_aggregate(
    agg_path: str,
    vitae_paths: List[str],
) -> AggregateContent:
    assert str(agg_path).endswith(".toml"), (
        "must be TOML files with .toml extension.")
    assert all(path.endswith(".toml") for path in vitae_paths), (
        "must be TOML files with .toml extension.")

    with open(agg_path) as src:
        aggr = AggregateContent(**toml.load(src))

    # transpose technical skill: [{s1}, {s1, s2}] -> {s1:2, s2:1}
    vitaes = [load_vitae(path) for path in vitae_paths]
    technical_skills: Dict[str, int] = defaultdict(int)
    for vitae in vitaes:
        for skill in vitae.technical_skill:
            for value in skill.values:
                technical_skills[value] += 1

    skills = get_skills_data()["skills"]
    unknown_skills = set(aggr.technical_skills).difference(skills)
    assert not unknown_skills, f"unallowed skills: {unknown_skills}"

    values = sorted(technical_skills.keys())
    aggr.skill_count = [
        SkillCount(value=value, count=technical_skills[value])
        for value in values
        if value in aggr.technical_skills
    ]

    # anything with meta.*_image should be an image
    for name in aggr.meta.__dict__:
        if not name.endswith("_image"):
            continue
        value = getattr(aggr.meta, name)
        if not os.path.isfile(value):
            setattr(aggr.meta, name, os.path.join(
                CURDIR, os.path.pardir, "templates", f"{value}.pdf"))
            assert os.path.isfile(getattr(aggr.meta, name)), (
                f"unrecognized value/path for meta.{name}: '{value}'")

    return aggr
