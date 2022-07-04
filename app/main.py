from fastapi import FastAPI, Request
from models.models import database, metadata, engine

from routers import users_router, permissions_router, groups_router


tags_metadata = [
    {
        "name": "Users",
        "description": "Users",
    },
]

app = FastAPI(
    title="Users and groups",
    docs_url=f"/ehouse/api/users/docs/",
    openapi_url=f"/ehouse/api/users/openapi.json",
    openapi_tags=tags_metadata,
)

app.include_router(users_router)
app.include_router(permissions_router)
app.include_router(groups_router)


@app.get("/ehouse/api/users")
async def root(request: Request):
    # print(request.user)
    return {"message": "users"}


@app.on_event("startup")
async def startup() -> None:
    # database_ = app.state.database
    # metadata.create_all(engine)
    if not database.is_connected:
        await database.connect()
