from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[int]
    name: str = Field(min_length=2, max_length=100)
    username: str = Field(min_length=2, max_length=100)
    email: str  = Field(min_length=11, max_length=500)
    password: str = Field(min_length=3, max_length=100)