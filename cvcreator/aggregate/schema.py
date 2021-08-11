"""Create aggregated values."""
from typing import List
from pydantic import BaseModel, Field

from ..vitae.schema import TechnicalSkill


class SkillCount(BaseModel):
    """Skills and their count."""
    value: str
    count: int


class MetaInformation(BaseModel):
    """Meta-information used by the document."""

    font_size: int = 11
    logo_image: str = "logo"
    footer_image: str = "footer"


class AggregateContent(BaseModel):
    """Schema for Aggregate content file."""

    summary: str = ""

    meta: MetaInformation = MetaInformation()

    technical_skills: List[str]
    skill_count: List[SkillCount] = Field(default_factory=list)
