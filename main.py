from fastapi import FastAPI, Depends
from db.models import User
from fastapi_users import fastapi_users, FastAPIUsers
from api.cfg import auth_backend
from api.manager import get_user_manager
from api.schemas import UserCreate, UserRead


app = FastAPI()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

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

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"

# @app.get("/salary", response_model=Salary)
# async def get_salary(
#     current_user: User = current_user,
# ):
#     salary = await get_db().get(Salary, user_id=current_user.id)
#     if salary:
#         return salary
#     else:
#         raise HTTPException(status_code=404, detail="Salary not found")


# @app.post("/salary", response_model=Salary)
# async def create_salary(
#     amount: int,
#     current_user: User = current_user,
#     db: Session = Depends(get_db)
# ):
#     salary = Salary(amount=amount, user_id=current_user.id)
#     get_db().add(salary)
#     get_db().commit()
#     get_db().refresh(salary)
#     return salary
