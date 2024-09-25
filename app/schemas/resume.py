from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr


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


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(ExperienceBase):
    id: Optional[int] = None


class Experience(ExperienceBase):
    id: int
    resume_id: int

    class Config:
        orm_mode = True


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


class Education(EducationBase):
    id: int
    resume_id: int

    class Config:
        orm_mode = True


class LanguageSkillBase(BaseModel):
    language: str
    other_languages:Optional[str] =None
    # is_mother_tongue: bool = False
    # proficiency_level: Optional[str] = None


class LanguageSkillCreate(LanguageSkillBase):
    pass


class LanguageSkillUpdate(LanguageSkillBase):
    id: Optional[int] = None


class LanguageSkill(LanguageSkillBase):
    id: int
    resume_id: int

    class Config:
        orm_mode = True


class DrivingLicenseBase(BaseModel):
    license_type: str
    license_issued_date: date
    license_expiry_date: date


class DrivingLicenseCreate(DrivingLicenseBase):
    pass

class DrivingLicenseUpdate(DrivingLicenseBase):
    id: Optional[int] = None


class DrivingLicense(DrivingLicenseBase):
    id: int
    resume_id: int

    class Config:
        orm_mode = True


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



class TrainingAward(TrainingAwardBase):
    id: int
    resume_id: int

    class Config:
        orm_mode = True


class OthersBase(BaseModel):
    sectiontitle: str
    title: str
    description: str


class OthersCreate(OthersBase):
    pass

class OthersUpdate(OthersBase):
    id: Optional[int] = None



class Others(OthersBase):
    id: int
    resume_id: int

    class Config:
        orm_mode = True


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
    email_address: Optional[EmailStr]
    contact_number: Optional[str]
    responsibilities: Optional[str]
    referred_by: Optional[str] = "RSR Academy"


class ResumeCreate(BaseModel):
    resume_title: str


class ResumeUpdate(ResumeBase):
    pass


class Resume(ResumeBase):
    id: int
    user_id: int
    resume_image: Optional[str]
    experiences: Optional[List[Experience]] 
    education: Optional[List[Education]] 
    language_skills: Optional[List[LanguageSkill]] 
    driving_license: Optional[List[DrivingLicense]] 
    training_awards: Optional[List[TrainingAward]] 
    others: Optional[List[Others]] 

    class Config:
        from_attributes = True
