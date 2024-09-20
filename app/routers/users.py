from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_async_db
from app.dependencies.auth import get_current_user
from app.models.users import User
from app.schemas.users import UserBaseSchema, UserDetailSchema

router = APIRouter(prefix="/users", tags=["Users"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
user_dep = Annotated[dict,Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK, response_model=Optional[list[UserBaseSchema]])
async def get_all_users(db:db_dep):

    users =await  User.get_all(db, [])

    return users

@router.get("/me", status_code=status.HTTP_200_OK, response_model=Optional[UserDetailSchema])
async def get_current_login_user(db:db_dep, current_user:user_dep):

    user =await  User.get_one(db, [User.id == current_user.get('id')])

    return user