from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class PersonalInfoBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class PersonalInfoCreate(PersonalInfoBase):
    pass

class PersonalInfo(PersonalInfoBase):
    id: int

    class Config:
        orm_mode = True

class ExperienceBase(BaseModel):
    company: str
    position: str
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None

class ExperienceCreate(ExperienceBase):
    pass

class Experience(ExperienceBase):
    id: int
    resume_id: int

    class Config:
        orm_mode = True

class EducationBase(BaseModel):
    institution: str
    degree: str
    field: str
    start_date: date
    end_date: Optional[date] = None

class EducationCreate(EducationBase):
    pass

class Education(EducationBase):
    id: int
    resume_id: int

    class Config:
        orm_mode = True

class ResumeBase(BaseModel):
    pass

class ResumeCreate(ResumeBase):
    personal_info: PersonalInfoCreate
    experiences: List[ExperienceCreate] = []
    education: List[EducationCreate] = []

class ResumeUpdate(ResumeBase):
    personal_info: PersonalInfoBase
    experiences: List[ExperienceBase] = []
    education: List[EducationBase] = []

class Resume(ResumeBase):
    id: int
    personal_info: PersonalInfo
    experiences: List[Experience] = []
    education: List[Education] = []

    class Config:
        orm_mode = True
