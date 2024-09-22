from datetime import date
from typing import Any, List, Optional

from sqlalchemy import ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base
from app.models.stripe_payment import StripePayment
from app.models.users import User


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    resume_title: Mapped[str] 

    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    date_of_birth: Mapped[Optional[date]]
    nationality: Mapped[Optional[str]]
    address_line_1: Mapped[Optional[str]]
    address_line_2: Mapped[Optional[str]]
    postal_code: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    country: Mapped[Optional[str]]
    email_address: Mapped[Optional[str]]
    contact_number: Mapped[Optional[str]]
    responsibilities: Mapped[Optional[str]]
    referred_by: Mapped[Optional[str]]= mapped_column(default="RSR Academy")

    
    experiences: Mapped[List["Experience"]] = relationship(back_populates="resume", cascade="all, delete-orphan" , lazy='selectin')
    education: Mapped[List["Education"]] = relationship(back_populates="resume", cascade="all, delete-orphan", lazy='selectin')
    language_skills: Mapped[List["LanguageSkill"]] = relationship(back_populates="resume", cascade="all, delete-orphan",  lazy='selectin')
    driving_license: Mapped[List["DrivingLicense"]] = relationship(back_populates="resume", cascade="all, delete-orphan",  lazy='selectin')
    training_awards: Mapped[List["TrainingAward"]] = relationship(back_populates="resume", cascade="all, delete-orphan",  lazy='selectin')
    others: Mapped[List["Others"]] = relationship(back_populates="resume", cascade="all, delete-orphan", lazy='selectin')
    # stripe_payments: Mapped[List["StripePayment"]] = relationship(back_populates="resume",)
    user: Mapped["User"] = relationship(back_populates="resumes")

    @classmethod
    async def create(cls, db: AsyncSession, user_id: int, **kwargs):
        resume = cls(**kwargs, user_id=user_id)
        db.add(resume)
        await db.commit()
        await db.refresh(resume)
        return resume

    @classmethod
    async def get_one(cls, db: AsyncSession, where_conditions: list[Any]):
        query = select(cls)
        if where_conditions:
            query = query.filter(*where_conditions)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, db: AsyncSession, skip: int = 0, limit: int = 100, where_conditions: list[Any] = []):
        query = select(cls).offset(skip).limit(limit)
        if where_conditions:
            query = query.filter(*where_conditions)
        result = await db.execute(query)
        return result.scalars().all()

    async def update(self, db: AsyncSession, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        await db.commit()
        await db.refresh(self)
        return self

    async def delete(self, db: AsyncSession):
        await db.delete(self)
        await db.commit()

class Experience(Base):
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"))

    employer: Mapped[str] = mapped_column(index=True)
    website: Mapped[Optional[str]]
    location: Mapped[str]
    occupation: Mapped[str]
    from_date: Mapped[date]
    to_date: Mapped[Optional[date]]
    currently_working: Mapped[bool] = mapped_column(default=False)
    about_company: Mapped[Optional[str]]
    responsibilities: Mapped[str]
    
    resume: Mapped["Resume"] = relationship(back_populates="experiences")


    @classmethod
    async def create(cls, db: AsyncSession, resume_id: int, **kwargs):
        experience = cls(**kwargs, resume_id=resume_id)
        db.add(experience)
        await db.commit()
        await db.refresh(experience)
        return experience
    
    @classmethod
    async def get_one(cls, db: AsyncSession, where_conditions: list[Any]):
        query = select(cls)
        if where_conditions:
            query = query.filter(*where_conditions)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def update(self, db: AsyncSession, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        await db.commit()
        await db.refresh(self)
        return self

    async def delete(self, db: AsyncSession):
        await db.delete(self)
        await db.commit()

class Education(Base):
    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"))

    title_of_qualification: Mapped[str]
    organization_name: Mapped[str]
    from_date: Mapped[date]
    to_date: Mapped[Optional[date]]
    city: Mapped[str]
    country: Mapped[str]

    resume: Mapped["Resume"] = relationship(back_populates="education")

    @classmethod
    async def create(cls, db: AsyncSession, resume_id: int, **kwargs):
        education = cls(**kwargs, resume_id=resume_id)
        db.add(education)
        await db.commit()
        await db.refresh(education)
        return education    

    @classmethod
    async def get_one(cls, db: AsyncSession, where_conditions: list[Any]):
        query = select(cls)
        if where_conditions:
            query = query.filter(*where_conditions)
        result = await db.execute(query)
        return result.scalar_one_or_none()
        

    @classmethod        
    async def get_all(cls, db: AsyncSession, skip: int = 0, limit: int = 100, where_conditions: list[Any] = []):
        query = select(cls).offset(skip).limit(limit)
        if where_conditions:
            query = query.filter(*where_conditions)
        result = await db.execute(query)
        return result.scalars().all()

    async def update(self, db: AsyncSession, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        await db.commit()
        await db.refresh(self)
        return self

    async def delete(self, db: AsyncSession):
        await db.delete(self)
        await db.commit()


class LanguageSkill(Base):
    __tablename__ = "language_skills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"))

    language: Mapped[str]
    is_mother_tongue: Mapped[bool] = mapped_column(default=False)
    proficiency_level: Mapped[Optional[str]]

    resume: Mapped["Resume"] = relationship(back_populates="language_skills")

    @classmethod
    async def create(cls, db: AsyncSession, resume_id: int, **kwargs):
        language_skill = cls(**kwargs, resume_id=resume_id)
        db.add(language_skill)
        await db.commit()
        await db.refresh(language_skill)
        return language_skill

    @classmethod
    async def get_one(cls, db: AsyncSession, where_conditions: list[Any]):
        query = select(cls)
        if where_conditions:
            query = query.filter(*where_conditions)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, db: AsyncSession, skip: int = 0, limit: int = 100, where_conditions: list[Any] = []):    
        query = select(cls).offset(skip).limit(limit)
        if where_conditions:
            query = query.filter(*where_conditions)
        result = await db.execute(query)
        return result.scalars().all()

    async def update(self, db: AsyncSession, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)   
        await db.commit()
        await db.refresh(self)
        return self

    async def delete(self, db: AsyncSession):
        await db.delete(self)
        await db.commit()

class DrivingLicense(Base):
    __tablename__ = "driving_licenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"))

    license_type: Mapped[str]
    license_issued_date: Mapped[date]
    license_expiry_date: Mapped[date]
  
   
    resume: Mapped["Resume"] = relationship(back_populates="driving_license")

    @classmethod
    async def create(cls, db: AsyncSession, resume_id: int, **kwargs):
        language_skill = cls(**kwargs, resume_id=resume_id)
        db.add(language_skill)
        await db.commit()
        await db.refresh(language_skill)
        return language_skill

    @classmethod
    async def get_one(cls, db: AsyncSession, where_conditions: list[Any]):
        query = select(cls)
        if where_conditions:
            query = query.filter(*where_conditions)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, db: AsyncSession, skip: int = 0, limit: int = 100, where_conditions: list[Any] = []):    
        query = select(cls).offset(skip).limit(limit)
        if where_conditions:
            query = query.filter(*where_conditions)
        result = await db.execute(query)
        return result.scalars().all()

    async def update(self, db: AsyncSession, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)   
        await db.commit()
        await db.refresh(self)
        return self

    async def delete(self, db: AsyncSession):
        await db.delete(self)
        await db.commit()

    

class TrainingAward(Base):
    __tablename__ = "training_awards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"))

    title: Mapped[str]
    awarding_institute: Mapped[str]
    from_date: Mapped[date]
    to_date: Mapped[Optional[date]]
    location: Mapped[str]

    resume: Mapped["Resume"] = relationship(back_populates="training_awards")

    @classmethod
    async def create(cls, db: AsyncSession, resume_id: int, **kwargs):
        language_skill = cls(**kwargs, resume_id=resume_id)
        db.add(language_skill)
        await db.commit()
        await db.refresh(language_skill)
        return language_skill

    @classmethod
    async def get_one(cls, db: AsyncSession, where_conditions: list[Any]):
        query = select(cls)
        if where_conditions:
            query = query.filter(*where_conditions)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, db: AsyncSession, skip: int = 0, limit: int = 100, where_conditions: list[Any] = []):    
        query = select(cls).offset(skip).limit(limit)
        if where_conditions:
            query = query.filter(*where_conditions)
        result = await db.execute(query)
        return result.scalars().all()

    async def update(self, db: AsyncSession, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)   
        await db.commit()
        await db.refresh(self)
        return self

    async def delete(self, db: AsyncSession):
        await db.delete(self)
        await db.commit()

class Others(Base):
    __tablename__ = "others"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"))

    sectiontitle: Mapped[str]
    title: Mapped[str]
    description: Mapped[str]

    resume: Mapped["Resume"] = relationship(back_populates="others")

    @classmethod
    async def create(cls, db: AsyncSession, resume_id: int, **kwargs):
        language_skill = cls(**kwargs, resume_id=resume_id)
        db.add(language_skill)
        await db.commit()
        await db.refresh(language_skill)
        return language_skill

    @classmethod
    async def get_one(cls, db: AsyncSession, where_conditions: list[Any]):
        query = select(cls)
        if where_conditions:
            query = query.filter(*where_conditions)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, db: AsyncSession, skip: int = 0, limit: int = 100, where_conditions: list[Any] = []):    
        query = select(cls).offset(skip).limit(limit)
        if where_conditions:
            query = query.filter(*where_conditions)
        result = await db.execute(query)
        return result.scalars().all()

    async def update(self, db: AsyncSession, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)   
        await db.commit()
        await db.refresh(self)
        return self

    async def delete(self, db: AsyncSession):
        await db.delete(self)
        await db.commit()