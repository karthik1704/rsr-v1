from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

    
from .users import User