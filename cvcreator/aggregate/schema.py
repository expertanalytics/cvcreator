"""Create aggregated values."""
from typing import List
from pydantic import BaseModel, Field

from ..vitae.schema import TechnicalSkill


class SkillCount(BaseModel):
    """Skills and their count."""
    value: str
    count: int


class TopicCount(BaseModel):
    """Field of research and their count."""
    value: str
    count: int


class AggregateContent(BaseModel):
    """Schema for Aggregate content file."""

    technical_skills: List[str]
    topics: List[str]

    num_employees: int = 0
    num_doctors: int = 0
    num_nationalities: int = 0
    num_languages_spoken: int = 0
    num_universities_attended: int = 0

    skill_count: List[SkillCount] = Field(default_factory=list)
    topic_count: List[TopicCount] = Field(default_factory=list)
