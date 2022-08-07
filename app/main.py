from fastapi import FastAPI, Request
from models.db import Base, engine

# from services import audit_crud

# from routers__1 import permissions_router

from routers import groups_routers, permissions_routers, users_routers, audit_routers


tags_metadata = [
    {
        "name": "Users",
        "description": "Users",
    },
    {
        "name": "Groups",
        "description": "Groups",
    },
    {
        "name": "Permissions",
        "description": "Permissions",
    },
    {
        "name": "Audit",
        "description": "Audit Services",
    },
]

app = FastAPI(
    title="Users and groups",
    docs_url=f"/ehouse/api/auth/docs/",
    openapi_url=f"/ehouse/api/auth/openapi.json",
    openapi_tags=tags_metadata,
)


app.include_router(users_routers.users_router)
app.include_router(permissions_routers.permissions_router)
app.include_router(groups_routers.groups_router)
app.include_router(audit_routers.audit_router)
