"""Group skills into categories."""
import os
from typing import Any, Dict, List, Sequence
from collections import defaultdict

import toml

from .schema import TechnicalSkill, SkillCategory

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

    _validate_skills(skills, skills_data)

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
        output[key] = mapping.pop(key)

    output = [TechnicalSkill(title=title, values=output[title])
              for title in skills_data["allowed_labels"] if title in output]
    return output


def get_skills(skill_categories: List[SkillCategory]) -> List[TechnicalSkill]:
    """Process skills organized in skill categories into a list of `TechnicalSkill` objects

    Args:
        skill_categories:
            User provided skills to distribute into groups.

    Returns:
        List of TechnicalSkill objects
    """
    output: List[TechnicalSkill] = []

    # Get technical skills data
    skills_data = get_skills_data()

    # Process the skill categories in the CV
    for skill_category in skill_categories:
        label = skill_category.category
        skills = skill_category.technical_skills
        # Validation of skill categories and skills
        if label not in skills_data["allowed_labels"]:
            raise ValueError(f"{label}: Invalid skill label")
        _validate_skills(skills, skills_data)

        output.append(TechnicalSkill(title=label, values=skills))

    return output


def _validate_skills(skills: Sequence[str], skills_data: dict[str, Any]):
    """Check that skills are valid.

    Compare a list of skill strings against a data structure containing allowed skills.

    Args:
        skills:
             List of skills.
        skills_data:
            Technical skills data.
    """
    unknown_skills = set(skills).difference(skills_data["skills"])
    assert not unknown_skills, (
        f"unrecognized technical skills: {sorted(unknown_skills)}"
        "\nPrint out all available technical skills with `cv skills`")
