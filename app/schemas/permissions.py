from typing import List, Optional
from pydantic.main import BaseModel
from models import models


class PermissionCreate(models.Permission.get_pydantic(exclude={"id", "groups"})):
    groups: Optional[List[str]] = []
