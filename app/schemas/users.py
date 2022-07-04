from datetime import datetime
from typing import List

from pydantic.main import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
