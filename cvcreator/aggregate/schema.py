"""Create aggregated values."""
from typing import List
from pydantic import BaseModel, Field

from ..vitae.schema import TechnicalSkill


class SkillCount(BaseModel):
    """Skills and their count."""
    value: str
    count: int


class AggregateContent(BaseModel):
    """Schema for Aggregate content file."""

    technical_skills: List[str]

    skill_count: List[SkillCount] = Field(default_factory=list)
