# pylint: disable=too-few-public-methods
"""Schema definition for the user provided yaml source file."""
import datetime
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field
import pycountry


COUNTRIES = tuple(country.__dict__.get(
    "common_name", country.name).replace(", Islamic Republic of", "")
    for country in pycountry.countries)
Country = Literal[COUNTRIES]

LANGUAGES = tuple(language.name for language in pycountry.languages)
Language = Literal[LANGUAGES]

# hopefully exhaustive:
NATIONALITIES = (
    'Afghan', 'Albanian', 'Algerian', 'American', 'Andorran', 'Angolan',
    'Antiguans', 'Argentinean', 'Armenian', 'Australian', 'Austrian',
    'Azerbaijani', 'Bahamian', 'Bahraini', 'Bangladeshi', 'Barbadian',
    'Barbudans', 'Batswana', 'Belarusian', 'Belgian', 'Belizean', 'Beninese',
    'Bhutanese', 'Bolivian', 'Bosnian', 'Brazilian', 'British', 'Bruneian',
    'Bulgarian', 'Burkinabe', 'Burmese', 'Burundian', 'Cambodian',
    'Cameroonian', 'Canadian', 'Cape Verdean', 'Central African', 'Chadian',
    'Chilean', 'Chinese', 'Colombian', 'Comoran',  'Congolese', 'Costa Rican',
    'Croatian', 'Cuban', 'Cypriot', 'Czech', 'Danish', 'Djibouti', 'Dominican',
    'Dutch', 'Dutchman', 'Dutchwoman', 'East Timorese', 'Ecuadorean',
    'Egyptian', 'Emirian', 'Equatorial Guinean', 'Eritrean', 'Estonian',
    'Ethiopian', 'Fijian', 'Filipino', 'Finnish', 'French', 'Gabonese',
    'Gambian', 'Georgian', 'German', 'Ghanaian', 'Greek', 'Grenadian',
    'Guatemalan', 'Guinea-Bissauan', 'Guinean', 'Guyanese', 'Haitian',
    'Herzegovinian', 'Honduran', 'Hungarian', 'I-Kiribati', 'Icelander',
    'Indian', 'Indonesian', 'Iranian', 'Iraqi', 'Irish', 'Israeli', 'Italian',
    'Ivorian', 'Jamaican', 'Japanese', 'Jordanian', 'Kazakhstani', 'Kenyan',
    'Kittian and Nevisian', 'Kuwaiti', 'Kyrgyz', 'Laotian', 'Latvian',
    'Lebanese', 'Liberian', 'Libyan', 'Liechtensteiner', 'Lithuanian',
    'Luxembourger', 'Macedonian', 'Malagasy', 'Malawian', 'Malaysian',
    'Maldivan', 'Malian', 'Maltese', 'Marshallese', 'Mauritanian', 'Mauritian',
    'Mexican', 'Micronesian', 'Moldovan', 'Monacan', 'Mongolian', 'Moroccan',
    'Mosotho', 'Motswana', 'Mozambican', 'Namibian', 'Nauruan', 'Nepalese',
    'Netherlander', 'New Zealander', 'Ni-Vanuatu', 'Nicaraguan', 'Nigerian',
    'Nigerien', 'North Korean', 'Northern Irish', 'Norwegian', 'Omani',
    'Pakistani', 'Palauan', 'Panamanian', 'Papua New Guinean', 'Paraguayan',
    'Peruvian', 'Polish', 'Portuguese', 'Qatari', 'Romanian', 'Russian',
    'Rwandan', 'Saint Lucian', 'Salvadoran', 'Samoan', 'San Marinese',
    'Sao Tomean', 'Saudi', 'Scottish', 'Senegalese', 'Serbian', 'Seychellois',
    'Sierra Leonean', 'Singaporean', 'Slovakian', 'Slovenian',
    'Solomon Islander', 'Somali', 'South African', 'South Korean', 'Spanish',
    'Sri Lankan', 'Sudanese', 'Surinamer', 'Swazi', 'Swedish', 'Swiss',
    'Syrian', 'Taiwanese', 'Tajik', 'Tanzanian', 'Thai', 'Togolese', 'Tongan',
    'Trinidadian or Tobagonian', 'Tunisian', 'Turkish', 'Tuvaluan', 'Ugandan',
    'Ukrainian', 'Uruguayan', 'Uzbekistani', 'Venezuelan', 'Vietnamese',
    'Welsh', 'Yemenite', 'Zambian', 'Zimbabwean'
)
Nationality = Literal[NATIONALITIES]


class StrictModel(BaseModel):
    """Same as baseclass, but forbit superfluous variables."""

    class Config:
        extra = "forbid"


class TechnicalSkill(StrictModel):
    """Group of technical skills."""

    title: str
    values: List[str]


class LanguageSkill(StrictModel):
    """Language skill and proficiency."""

    language: Language
    proficiency: Literal["Native", "Fluent", "Intermediate", "Basic"]


class PersonalSkill(StrictModel):
    """A personal skill and description."""

    title: str
    description: str


class Hobby(StrictModel):
    """Group of hobbies."""

    title: str
    values: List[str]


class Education(StrictModel):
    """Completed educational degree."""

    start: int = 0
    end: int = 0
    degree: Literal["Bachelor's degree", "Master's degree", "PhD",
                    "Diploma degree", "Cand. Scient", "Doctor Scient", ""] = ""
    topic: Literal["Physics", "Scientific Computing", "Mechanics",
                   "Mathematics", "Engineering", "Chemestry",
                   "Geology and Geophysics", "Computer Science", ""] = ""
    specialization: str = ""
    thesis_title: str = ""
    department: str = ""
    university: str = ""
    country: Country = ""
    description: str = ""


class Work(StrictModel):
    """Previous work experience."""

    start: str
    end: str = ""
    description: str


class Project(StrictModel):
    """Extended description of a project."""

    activity: str
    role: str = ""
    staffing: str = ""
    period: str = ""
    description: str
    tools: str = ""
    volume: str = ""
    url: str = ""
    tag: str = ""


class Publications(StrictModel):
    """Published journal papers."""

    journal: str
    title: str
    doi: str
    authors: str
    year: int
    tag: str = ""
    description: str = ""


class MetaInformation(StrictModel):
    """Meta-information used by the document."""

    font_size: int = 11
    logo_image: str = "logo"
    footer_image: str = "footer"
    email_image: str = "email"
    address_image: str = "address"
    github_image: str = "link"
    website_image: str = "link"
    phone_image: str = "phone"
    birth_image: str = "birth"
    nationality_image: str = "nationality"


class VitaeContent(StrictModel):
    """Schema for Vitae content file."""

    name: str
    address: str = ""
    post: str = ""
    birth: Optional[datetime.date] = None
    email: str = ""
    phone: str = ""
    nationality: Optional[Nationality] = None
    github: str = ""
    website: str = ""
    summary: str = ""

    meta: MetaInformation = MetaInformation()

    # Should be TechnicalSkill, but is constructed after parsing.
    # 'str' is used here as a placeholder for list of skills.
    technical_skill: Union[List[str], List[TechnicalSkill]] = (
        Field(default_factory=list))

    language_skill: List[LanguageSkill] = Field(default_factory=list)
    personal_skill: List[PersonalSkill] = Field(default_factory=list)
    hobby: List[Hobby] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    work: List[Work] = Field(default_factory=list)
    project: List[Project] = Field(default_factory=list)
    publication: List[Publications] = Field(default_factory=list)
