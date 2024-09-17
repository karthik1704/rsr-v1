from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional

from sqlalchemy import DateTime, ForeignKey, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship

from app.helpers.fields import DefaultFieldsMixin
from app.models import Base

if TYPE_CHECKING:
    from app.models.resume import Resume
    from app.models.stripe_payment import StripePayment


class User(Base, DefaultFieldsMixin):
    __tablename__ = "users"

    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    phone: Mapped[str]

    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    stripe_payments: Mapped[List["StripePayment"]] = relationship(back_populates="user")
    resumes: Mapped[List["Resume"]] = relationship(back_populates="user")
    @classmethod
    async def get_all(cls, db_session:AsyncSession, where_conditon:list[Any]):
        _stmt = select(cls).where(*where_conditon).order_by(desc(cls.id))
        _results = await db_session.execute(_stmt)
        return _results.scalars()
    
    @classmethod
    async def get_one(cls, database_session: AsyncSession, where_conditions: list[Any]):
        _stmt = select(cls).where(*where_conditions)
        _result = await database_session.execute(_stmt)
        return _result.scalars().first()

    @classmethod
    async def create_user(cls, db: AsyncSession, desk):
        db.add(desk)

    def update_user(self, updated_data):
        for field, value in updated_data.items():
            setattr(self, field, value)