SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_JWT_SUBJECT = "access"
REFRESH_TOKEN_JWT_SUBJECT = "refresh"

EXPIRES_DELTA_ACCESS_TOKEN = 15
EXPIRES_DELTA_REFRESH_TOKEN = 30

TOKEN_TYPE = "bearer"

PASSWORD_TEMPLATE = r"^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d).*$"

# SQLALCHEMY_DATABASE_URL = (
#     "postgresql+asyncpg://ehouseuser:ehouse2022@db_ehouse_users/dbusers"
# )
SQLALCHEMY_DATABASE_URL = "postgresql://ehouseuser:ehouse2022@db_ehouse_users/dbusers"
