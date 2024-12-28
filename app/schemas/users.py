from datetime import datetime
from typing import Optional
from weakref import ref

from pydantic import BaseModel, EmailStr

from .stripe_payment import Payment


class UserBaseSchema(BaseModel):
    first_name:str
    last_name:str
    email: EmailStr
    phone: str
    referred_by: Optional[str] = None
   
class UserDetailSchema(UserBaseSchema):
    expiry_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    # payment_success: Optional[Payment] = None

class UserListSchema(UserBaseSchema):

    is_active: bool
    is_staff: bool
    is_superuser: bool

    created_at: datetime
    updated_at: datetime

class UserCreateSchema(UserBaseSchema):
    password:str
    password2: str


class Token(BaseModel):
    access_token:str
    token_type: str
    expiry_date: Optional[datetime] = None