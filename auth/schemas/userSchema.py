from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    class Config:
        orm_mode = True



class UserUpdate(BaseModel):
    id: int
    password: str
