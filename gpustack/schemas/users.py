from datetime import datetime
import re
from pydantic import field_validator
from sqlmodel import Field, SQLModel

from .common import PaginatedList
from ..mixins import BaseModelMixin


class UserBase(SQLModel):
    username: str
    is_admin: bool = False
    full_name: str | None = None


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    def validate_password(cls, value):
        if not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', value):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError('Password must contain at least one special character')
        return value


class UserUpdate(UserBase):
    password: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str

    @field_validator('new_password')
    def validate_password(cls, value):
        if not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', value):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError('Password must contain at least one special character')
        return value


class User(UserBase, BaseModelMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class UserPublic(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


UsersPublic = PaginatedList[UserPublic]
