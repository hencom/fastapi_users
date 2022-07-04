from typing import List, Optional
from pydantic.main import BaseModel
from models import models


class GroupCreate(models.Group.get_pydantic(exclude={"id", "permissions", "users"})):
    permissions: Optional[List[str]] = []
    # users: Optional[List[str]] = []
