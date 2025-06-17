from http import HTTPStatus
from fastapi import HTTPException
from fastapi_pagination import Page

from app.database import users
from app.models.User import UserData, UserDataCreateBody, UserDataUpdateBody

from fastapi import APIRouter


router = APIRouter(prefix="/api/users")


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> UserData:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user = users.get_user(user_id)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.get("/", status_code=HTTPStatus.OK)
def get_users() -> Page[UserData]:
    return users.get_users()


@router.post("/", status_code=201)
def create_user(user: UserData) -> UserData:
    UserDataCreateBody.model_validate(user.model_dump(mode="json"))
    return users.create_user(user)


@router.patch("/{user_id}", response_model=None)
def update_user(user_id: int, user_data: UserData):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalide user")
    UserDataUpdateBody.model_validate(user_data.model_dump())
    return users.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Incorrect user")
    users.delete_user(user_id)
    return {"message": "User deleted"}
