from fastapi import FastAPI, Depends, HTTPException
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase
from datetime import datetime, timedelta
from pydantic import BaseModel
from db.database import get_db, engine
from db.models import User, Salary
from dotenv import load_dotenv
import os


load_dotenv()

SECRET = os.environ.get('JWT_SECRET')
ALGORITHM = os.environ.get('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('JWT_EXPIRATION_MINUTES'))


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(models.BaseUserCreate):
    pass


class UserDB(models.BaseUserDB):
    pass


class UserUpdate(models.BaseUserUpdate):
    pass


class UserDBModel(UserDB, models.BaseUserDBModel):
    pass


user_db = SQLAlchemyUserDatabase(UserDBModel, engine, User)


def get_current_user(
    user: User = Depends(user_db.get_current_active_user)
) -> User:
    return user


def get_authentication():
    return JWTAuthentication(secret=SECRET, lifetime_seconds=ACCESS_TOKEN_EXPIRE_MINUTES * 60)


app = FastAPI()

fastapi_users = FastAPIUsers(
    user_db,
    [get_authentication()],
    User,
    UserCreate,
    UserUpdate,
    UserDBModel,
)


@app.on_event("startup")
async def startup():
    await user_db.create()


@app.on_event("shutdown")
async def shutdown():
    await user_db.close()
    await user_db.drop()


@app.post("/login", response_model=Token)
async def login(
    credentials: models.UserPasswordCredentials = Depends(fastapi_users.login),
):
    user = await user_db.get_by_email(credentials.email)
    access_token = get_authentication().generate_token(user)
    token_type = "bearer"
    return Token(access_token=access_token, token_type=token_type)


@app.get("/salary", response_model=Salary)
async def get_salary(
    current_user: User = Depends(get_current_user),
):
    salary = await get_db().get(Salary, user_id=current_user.id)
    if salary:
        return salary
    else:
        raise HTTPException(status_code=404, detail="Salary not found")


app.include_router(fastapi_users.router, prefix="/users", tags=["users"])