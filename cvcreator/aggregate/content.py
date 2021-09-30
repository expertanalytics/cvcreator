import os
from typing import Dict, List, Set
from collections import defaultdict

import toml

from ..vitae import load_vitae
from ..vitae.tech_skills import get_skills_data
from .schema import AggregateContent, SkillCount, TopicCount

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
    skill_count: Dict[str, int] = defaultdict(int)
    topic_count: Dict[str, int] = defaultdict(int)
    universities: Set[str] = set()
    nationalities: Set[str] = set()
    languages_spoken: Set[str] = set()
    for vitae in vitaes:
        for skill in vitae.technical_skill:
            for value in skill.values:
                skill_count[value] += 1

        for topic in set(edu.topic for edu in vitae.education):
            if topic:
                topic_count[topic] += 1

        aggr.num_doctors += any(edu.degree in ("PhD", "Doctor Scient")
                                for edu in vitae.education)
        universities.update(edu.university for edu in vitae.education)
        if vitae.nationality:
            nationalities.add(vitae.nationality)
        languages_spoken.update(lan.language for lan in vitae.language_skill)

    skills = get_skills_data()["skills"]
    unknown_skills = set(aggr.technical_skills).difference(skills)
    assert not unknown_skills, f"unallowed skills: {unknown_skills}"

    aggr.skill_count = [
        SkillCount(value=value, count=skill_count[value])
        for value in sorted(skill_count.keys())
        if value in aggr.technical_skills
    ]
    aggr.topic_count = [
        TopicCount(value=value, count=topic_count[value])
        for value in sorted(topic_count.keys())
        if value in aggr.topics
    ]
    aggr.num_employees = len(vitaes)
    aggr.num_nationalities = len(nationalities)
    aggr.num_languages_spoken = len(languages_spoken)
    aggr.num_universities_attended = len(universities)

    return aggr
