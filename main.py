from fastapi import FastAPI, Depends, HTTPException
from fastapi_users import fastapi_users, FastAPIUsers
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.cfg import auth_backend
from api.manager import get_user_manager
from api.schemas import UserCreate, UserRead, SalaryRead
from db.database import get_async_session
from db.models import User, Salary


app = FastAPI()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/salary", tags=["Salary"])
async def get_salary(current_user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    query = select(Salary).where(Salary.user_id == current_user.id)
    salary = await db.execute(query)
    salary = salary.scalar_one_or_none()

    if salary:
        return salary
    else:
        raise HTTPException(status_code=404, detail="Salary not found")


@app.post("/salary", tags=["Salary"]) 
async def create_salary(
    amount: int,
    current_user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session)
):
    salary = Salary(amount=amount, user_id=current_user.id)
    db.add(salary)
    await db.commit()
    return salary


# роут просто для проверки
@app.post("/protected-route", tags=["JWT login check"])
def login_check(user: User = Depends(current_user)):
    return f"Hello, {user.username}"