from typing import Optional
from typing_extensions import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from datetime import datetime, date

from db.database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    email: Mapped[str]
    username: Mapped[str] = mapped_column(index=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Salary(Base):
    __tablename__ = 'salaries'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[intpk] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[int]
    next_raise_date: Mapped[Optional[date]]