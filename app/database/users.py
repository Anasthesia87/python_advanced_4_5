from typing import Iterable

from fastapi import HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

from .engine import engine
from app.models.User import UserData
from sqlmodel import Session, select


def get_user(user_id: int) -> UserData | None:
    with Session(engine) as session:
        return session.get(UserData, user_id)


def get_users() -> Page[UserData]:
    with Session(engine) as session:
        statement = select(UserData)
        return paginate(session, statement)


def create_user(user: UserData) -> UserData:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def update_user(user_id: int, user_data: UserData) -> UserData:
    with Session(engine) as session:
        db_user = session.get(UserData, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user = user_data.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user


def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(UserData, user_id)
        session.delete(user)
        session.commit()
