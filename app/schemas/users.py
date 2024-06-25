from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    first_name:str
    last_name:str
    email: EmailStr
    phone: str
    is_active: bool
    is_staff: bool
    is_superuser: bool

    created_at: datetime
    updated_at: datetime

class UserListSchema(UserBaseSchema):

    is_active: bool
    is_staff: bool
    is_superuser: bool

    created_at: datetime
    updated_at: datetime


class Token(BaseModel):
    access_token:str
    token_type: str