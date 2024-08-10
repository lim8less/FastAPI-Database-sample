from pydantic import BaseModel
from typing import Optional

# Pydantic schema for creating a user
class UserCreate(BaseModel):
    name: str
    email: str

# Pydantic schema for reading a user
class UserRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# Pydantic schema for creating an item
class ItemCreate(BaseModel):
    title: str
    description: str
    owner_id: int

# Pydantic schema for reading an item
class ItemRead(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int

    class Config:
        orm_mode = True
