from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

    
from .resume import (
    DrivingLicense,
    Education,
    LanguageSkill,
    Others,
    Resume,
    TrainingAward,
)
from .stripe_payment import StripePayment
from .users import User
