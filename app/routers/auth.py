from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..database import get_async_db
from ..models.users import User
from ..schemas.users import Token, UserBaseSchema, UserCreateSchema
from ..utils import create_access_token, get_hashed_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])
db_dep = Annotated[AsyncSession, Depends(get_async_db)]


class UserLogin(BaseModel):
    username: str
    password: str


async def authenticate_user(email: str, password: str, db:db_dep):
    user = await User.get_one(db, [User.email==email] )
    
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


@router.post("/", response_model=Token)
async def login_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dep,
):
    user =await  authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )
    
    token = create_access_token(
        user.email, user.id,  timedelta(minutes=30)
    )
    response.set_cookie(
        key="access_token",
        value=token,
        max_age=3600,
        secure=False,
        httponly=True,
        path="/",
        domain="localhost",
    )

    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", status_code=status.HTTP_200_OK)
async def get_token_for_user(user: UserLogin, db: db_dep):
    _user = await authenticate_user(user.username, user.password, db)

    # TODO: out exception handling to external module
    if not _user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # TODO: add refresh token
    _token = create_access_token(
        _user.email, _user.id,  timedelta(minutes=30)
    )
    return {"access_token": _token, "token_type": "bearer"}


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateSchema, db: db_dep):
    
    
    _user = user.model_dump()
    
    user_exists = await User.get_one(db, [User.email==_user.get('email')])
    if  user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User Alread Exists"
        )

    password =_user.pop('password')
    password2 =_user.pop('password2')

    if password != password2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Password Didn't macth"
        )
    
    new_user = User(**_user, password=get_hashed_password(password), is_active=True)

    db.add(new_user)
    await db.commit()



# @router.post("/logout", status_code=status.HTTP_201_CREATED, response_model=UserLogoutResponse)
# async def user_logout(user: UserLogout, request: Request, db_session: AsyncSession = Depends(get_db)):
#     _user: User = await User.find(db_session, [User.email == user.email])

#     # TODO: out exception handling to external module
#     if not _user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     # TODO: remove access token
#     _token = await unset_jwt(request)
#     return {"message": "logged out"}
