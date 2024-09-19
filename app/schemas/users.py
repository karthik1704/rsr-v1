from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    first_name:str
    last_name:str
    email: EmailStr
    phone: str
   


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