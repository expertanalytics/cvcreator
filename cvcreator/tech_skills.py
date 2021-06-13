"""Group skills into categories."""
import os
from typing import Dict, List, Sequence
from collections import defaultdict

import toml

from .schema import TechnicalSkill


CURDIR = os.path.dirname(os.path.abspath(__file__))


def make_skill_groups(
    skills: Sequence[str],
    threshold: int = 5,
    cut_below: bool = True,
) -> List[TechnicalSkill]:
    """
    Group skills into categories.

    Prioritizes small groups from unpopular labels to increases the likelihood
    the large and popular labels can take the "leftovers".

    Args:
        skills:
            User provided skills to distribute into groups.
        threshold:
            Prioritize making groups that are at least this size.
            Use `cut_below` to enforce.
        cut_below:
            Remove groups that does not meet the `threshold` criteria.

    Returns:
        Skills distributed over different groups.

    Examples:
        >>> make_skill_groups(  # doctest: +NORMALIZE_WHITESPACE
        ...     ["SQLite", "CVS", "Git", "pip"], threshold=1)
        {'Package managers': ['pip'],
         'Databases': ['SQLite'],
         'Version control': ['CVS', 'Git']}
        >>> make_skill_groups(["SQLite", "CVS", "Git", "pip"], threshold=2)
        {'Version control': ['CVS', 'Git'], 'Tools': ['SQLite', 'pip']}
        >>> make_skill_groups(["SQLite", "CVS", "Git", "pip"], threshold=3)
        {'Code management': ['CVS', 'Git', 'pip']}
        >>> make_skill_groups(["SQLite", "CVS", "Git", "pip"],
        ...     threshold=3, cut_below=False)
        {'Code management': ['CVS', 'Git', 'pip'], 'Tools': ['SQLite']}

    """
    with open(os.path.join(
            CURDIR, "templates", "tech_skills.toml")) as handler:
        data = toml.load(handler)

    # get general group label popularity
    count = defaultdict(int)
    for skill in data["skills"]:
        for label in data["skills"][skill]:
            count[label] += 1
    max_count = max(count.values())+1

    skills = list(skills)
    unknown_skills = set(skills).difference(data["skills"])
    assert not unknown_skills, (
            f"unrecognized technical skills: {sorted(unknown_skills)}")

    output = {}
    while skills:

        # make map from group label to skill
        mapping = defaultdict(list)
        for skill in skills:
            for label in data["skills"][skill]:
                mapping[label].append(skill)

        # sort based on primery size of group and secondary general popularity
        keys = sorted(mapping,
                      key=lambda k: max_count*len(mapping[k])+count[k])
        for key in keys:
            if len(mapping[key]) >= threshold:
                break
        else:
            # threshold criteria not met
            if cut_below:
                break

        skills = [skill for skill in skills if skill not in mapping[key]]
        output[key] = sorted(mapping.pop(key))

    output = [TechnicalSkill(title=title, values=values)
              for title, values in output.items()]
    return output
