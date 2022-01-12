"""Group skills into categories."""
import os
from typing import Any, Dict, List, Sequence
from collections import defaultdict

import toml

from .schema import TechnicalSkill

CURDIR = os.path.dirname(os.path.abspath(__file__))


def get_skills_data() -> Dict[str, Any]:
    """Get technical skills data."""
    with open(os.path.join(
            CURDIR, os.path.pardir, "data", "tech_skills.toml")) as handler:
        return toml.load(handler)


def make_skill_groups(
    skills: Sequence[str],
    threshold: int = 5,
    cut_below: bool = False,
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
        ...     ["SQLite", "CVS", "Git", "Pip"], threshold=1)
        [TechnicalSkill(title='Organize', values=['CVS', 'Git', 'Pip']), 
         TechnicalSkill(title='Databases', values=['SQLite'])]
        >>> make_skill_groups(  # doctest: +NORMALIZE_WHITESPACE
        ...     ["SQLite", "CVS", "Git", "Pip"], threshold=2)
        [TechnicalSkill(title='Tools', values=['SQLite']), 
         TechnicalSkill(title='Organize', values=['CVS', 'Git', 'Pip'])]

    """
    skills_data = get_skills_data()

    # get general group label popularity
    count = defaultdict(int)
    for skill in skills_data["skills"]:
        for label in skills_data["skills"][skill]:
            count[label] += 1
    max_count = max(count.values())+1

    skills = list(skills)
    unknown_skills = set(skills).difference(skills_data["skills"])
    assert not unknown_skills, (
            f"unrecognized technical skills: {sorted(unknown_skills)}"
            "\nPrint out all available technical skills with `cv skills`")

    output = {}
    while skills:

        # make map from group label to skill
        mapping = defaultdict(list)
        for skill in skills:
            for label in skills_data["skills"][skill]:
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

    output = [TechnicalSkill(title=title, values=output[title])
              for title in skills_data["allowed_labels"] if title in output]
    return output
