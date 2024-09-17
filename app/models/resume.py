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

    first_name: Mapped[str] = mapped_column(index=True)
    last_name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    phone: Mapped[Optional[str]]
    address: Mapped[Optional[str]]

    
    experiences: Mapped[List["Experience"]] = relationship(back_populates="resume")
    education: Mapped[List["Education"]] = relationship(back_populates="resume")
    stripe_payments: Mapped[List["StripePayment"]] = relationship(back_populates="resume")
    user: Mapped["User"] = relationship(back_populates="resumes")

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        resume = cls(**kwargs)
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
    company: Mapped[str] = mapped_column(index=True)
    position: Mapped[str]
    start_date: Mapped[date]
    end_date: Mapped[Optional[date]]
    description: Mapped[Optional[str]]
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"))

    resume: Mapped["Resume"] = relationship(back_populates="experiences")

class Education(Base):
    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    institution: Mapped[str] = mapped_column(index=True)
    degree: Mapped[str]
    field: Mapped[str]
    start_date: Mapped[date]
    end_date: Mapped[Optional[date]]
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"))

    resume: Mapped["Resume"] = relationship(back_populates="education")