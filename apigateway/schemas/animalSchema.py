from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class AnimalBase(BaseModel):
    name: str
    danger: bool
    wild:bool
    notify:bool = False
    
class AnimalCreated(AnimalBase):
    date_created:datetime
    last_modified:datetime

class Animal(AnimalCreated):
    id: int
    class Config:
        orm_mode = True


class AnimalUpdate(BaseModel):
    id: int
    name: Optional[str]
    danger: Optional[bool]
    wild:Optional[bool]
    notify:Optional[bool] = False
    
class AnimalUpdated(AnimalUpdate):
    last_modified:datetime
