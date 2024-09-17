from typing import Optional

from pydantic import BaseModel


class PaymentCreate(BaseModel):
    resume_id: int

    amount: int
    currency: str

class PaymentUpdate(BaseModel):
    payment_id: int
    status: str
    failure_code: Optional[str] = None
    failure_message: Optional[str] = None

class Payment(BaseModel):
    id: int
    amount: int
    currency: str
    status: str
    failure_code: Optional[str] = None
    failure_message: Optional[str] = None
    stripe_payment_intent_id: str

    class Config:
        orm_mode = True