from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Optional
from app.schemas.users import UserBaseSchema

from app.database import get_async_db
from app.models.users import User

router = APIRouter(prefix="/users", tags=["Users"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]


@router.get("/", status_code=status.HTTP_200_OK, response_model=Optional[list[UserBaseSchema]])
async def get_all_users(db:db_dep):

    users =await  User.get_all(db, [])

    return users