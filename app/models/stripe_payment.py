from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models import Base

if TYPE_CHECKING:
    from app.models.resume import Resume
    from app.models.users import User

class StripePayment(Base):
    __tablename__ = "stripe_payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    payment_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)
    amount: Mapped[int] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    stripe_payment_intent_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    failure_code: Mapped[Optional[str]] = mapped_column(String)
    failure_message: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    
    # Additional fields that might be useful
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    # payment_method: Mapped[Optional[str]] = mapped_column(String)
    # description: Mapped[Optional[str]] = mapped_column(String)
    # metadata: Mapped[Optional[str]] = mapped_column(String)  # JSON string to store additional info
    # refunded: Mapped[bool] = mapped_column(default=False)
    # refund_amount: Mapped[Optional[int]] = mapped_column()
    # receipt_url: Mapped[Optional[str]] = mapped_column(String)

    user: Mapped[Optional["User"]] = relationship(back_populates="stripe_payments")
    #resume: Mapped[Optional["Resume"]] = relationship(back_populates="stripe_payments")

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        payment = cls(**kwargs)
        db.add(payment)
        await db.commit()
        await db.refresh(payment)
        return payment
    
    @classmethod
    async def get(cls, db: AsyncSession, where_conditions: list = []):
        stmt = select(cls)
        if where_conditions:
            stmt = stmt.where(*where_conditions)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, db: AsyncSession, where_conditions: list = []):
        stmt = select(cls)
        if where_conditions:
            stmt = stmt.where(*where_conditions)
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def update(cls, db: AsyncSession, payment_id: int, **kwargs):
        payment = await cls.get(db, [cls.stripe_payment_intent_id == payment_id])
        if payment:
            for key, value in kwargs.items():
                setattr(payment, key, value)
            await db.commit()
            await db.refresh(payment)
        return payment

    @classmethod
    async def delete(cls, db: AsyncSession, id: int):
        payment = await cls.get(db, [cls.id == id])
        if payment:
            await db.delete(payment)
            await db.commit()
        return payment