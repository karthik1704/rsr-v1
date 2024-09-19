from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

    
from .resume import Resume
from .stripe_payment import StripePayment
from .users import User
