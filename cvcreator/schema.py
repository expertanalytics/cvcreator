"""Schema definition for the user provided yaml source file."""
from typing import List, Tuple
from pydantic import BaseModel, Field
import toml


class TechnicalSkill(BaseModel):
    """Group of technical skills."""

    title: str
    values: List[str]

class LanguageSkill(BaseModel):
    """Language skill and proficiency."""

    language: str
    proficiency: str

class PersonalSkill(BaseModel):
    """A personal skill and description."""

    title: str
    description: str

class Hobby(BaseModel):
    """Group of hobbies."""

    title: str
    values: List[str]

class Education(BaseModel):
    """Completed educational degree."""

    year: str
    description: str

class Work(BaseModel):
    """Previous work experience."""

    start: str
    end: str = ""
    description: str

class Project(BaseModel):
    """Extended description of a project."""

    activity: str
    role: str = ""
    staffing: str = ""
    period: str = ""
    description: str
    tools: str = ""
    tag: str = ""

class Publications(BaseModel):
    """Published journal papers."""

    journal: str
    title: str
    doi: str
    authors: str
    year: int
    tag: str = ""

class MetaInformation(BaseModel):
    """Meta-information used by the document."""

    font_size: int = 11
    logo_image: str = "logo"
    footer_image: str = "footer"
    email_image: str = "email"
    address_image: str = "address"
    github_image: str = "link"
    phone_image: str = "phone"
    birth_image: str = "birth"
    nationality_image: str = "nationality"


class VitaeContent(BaseModel):
    """Schema for the yaml source file."""

    name: str
    address: str = ""
    post: str = ""
    birth: str = ""
    email: str = ""
    phone: str = ""
    nationality: str = ""
    github: str = ""
    summary: str = ""

    meta: MetaInformation = MetaInformation()

    technical_skill: List[TechnicalSkill] = Field(default_factory=list)
    language_skill: List[LanguageSkill] = Field(default_factory=list)
    personal_skill: List[PersonalSkill] = Field(default_factory=list)
    hobby: List[Hobby] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    work: List[Work] = Field(default_factory=list)
    project: List[Project] = Field(default_factory=list)
    publication: List[Publications] = Field(default_factory=list)

    @staticmethod
    def load(path: str) -> "VitaeContent":
        with open(path) as src:
            return VitaeContent(**toml.load(src))
