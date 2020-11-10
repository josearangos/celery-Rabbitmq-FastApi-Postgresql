from typing import List, Optional
from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    username: EmailStr

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    class Config:
        orm_mode = True



class UserUpdate(BaseModel):
    id: int
    password: str
