from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr, field_validator

from app.models import Base


class ExperienceBase(BaseModel):
    employer: str
    website: Optional[str] = None
    location: str
    occupation: str
    from_date: date
    to_date: Optional[date] = None
    currently_working: bool = False
    about_company: Optional[str] = None
    responsibilities: str

    @field_validator('to_date', mode='before')
    def convert_empty_string_to_none(cls, v):
        if v == "":
            return None
        return v

class ExperienceCreate(ExperienceBase):
    pass



class ExperienceUpdate(ExperienceBase):
    id: Optional[int] = None

    @field_validator('id', mode='before')
    def convert_empty_string_to_none(cls, v):
        if v == "":
            return None
        return v

class ExperienceUpdateMulti(BaseModel):
    job_applied_for: str
    experiences:Optional[List[ExperienceUpdate]]

class Experience(ExperienceBase):
    id: int
    resume_id: int

  


class EducationBase(BaseModel):
    title_of_qualification: str
    organization_name: str
    from_date: date
    to_date: Optional[date] = None
    city: str
    country: str


class EducationCreate(EducationBase):
    pass


class EducationUpdate(EducationBase):
    id: Optional[int] = None

    @field_validator('id', mode='before')
    def convert_empty_string_to_none(cls, v):
        if v == "":
            return None
        return v

class EducationUpdateMulti(BaseModel):
    educations:List[EducationUpdate]

class Education(EducationBase):
    id: int
    resume_id: int

    class Config:
        from_attributes = True


class LanguageSkillBase(BaseModel):
    language: str
    other_languages:Optional[str] =None
    # is_mother_tongue: bool = False
    # proficiency_level: Optional[str] = None


class LanguageSkillCreate(LanguageSkillBase):
    pass


class LanguageSkillUpdate(LanguageSkillBase):
    id: Optional[int] = None

    @field_validator('id', mode='before')
    def convert_empty_string_to_none(cls, v):
        if v == "":
            return None
        return v


class LanguageSkill(LanguageSkillBase):
    id: int
    resume_id: int



class DrivingLicenseBase(BaseModel):
    license_type: str
    license_issued_date: date
    license_expiry_date: date


class DrivingLicenseCreate(DrivingLicenseBase):
    pass

class DrivingLicenseUpdate(DrivingLicenseBase):
    id: Optional[int] = None

    @field_validator('id', mode='before')
    def convert_empty_string_to_none(cls, v):
        if v == "":
            return None
        return v
    
class DrivingLicenseUpdateMulti(BaseModel):
    driving_licenses:List[DrivingLicenseUpdate]


class DrivingLicense(DrivingLicenseBase):
    id: int
    resume_id: int

  


class TrainingAwardBase(BaseModel):
    title: str
    awarding_institute: str
    from_date: date
    to_date: Optional[date] = None
    location: str


class TrainingAwardCreate(TrainingAwardBase):
    pass

class TrainingAwardUpdate(TrainingAwardBase):
    id: Optional[int] = None

    @field_validator('id', mode='before')
    def convert_empty_string_to_none(cls, v):
        if v == "":
            return None
        return v

class TrainingAwardUpdateMulti(BaseModel):
    training_awards:List[TrainingAwardUpdate]

class TrainingAward(TrainingAwardBase):
    id: int
    resume_id: int

    class Config:
        from_attributes = True


class OthersBase(BaseModel):
    sectiontitle: str
    title: str
    description: str


class OthersCreate(OthersBase):
    pass

class OthersUpdate(OthersBase):
    id: Optional[int] = None

    @field_validator('id', mode='before')
    def convert_empty_string_to_none(cls, v):
        if v == "":
            return None
        return v



class Others(OthersBase):
    id: int
    resume_id: int

    class Config:
        from_attributes = True


class ResumeBase(BaseModel):
    resume_title: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[date]
    nationality: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str] = None
    postal_code: Optional[str]
    city: Optional[str]
    country: Optional[str]
    email_address: Optional[EmailStr] = None
    contact_number: Optional[str]
    responsibilities: Optional[str]
    referred_by: Optional[str] = "RSR Academy"

    @field_validator('email_address', mode='before')
    def convert_empty_string_to_none(cls, v):
        if v == "":
            return None
        return v


class ResumeCreate(BaseModel):
    resume_title: str


class ResumeUpdate(ResumeBase):
    pass


class Resume(ResumeBase):
    id: int
    user_id: int
    job_applied_for: Optional[str]
    resume_image: Optional[str]
    experiences: Optional[List[Experience]] 
    education: Optional[List[Education]] 
    language_skills: Optional[LanguageSkill] 
    driving_license: Optional[List[DrivingLicense]] 
    training_awards: Optional[List[TrainingAward]] 
    others: Optional[List[Others]] 

    class Config:
        from_attributes = True
