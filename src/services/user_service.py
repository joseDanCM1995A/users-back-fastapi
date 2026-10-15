from fastapi import HTTPException

from src.store.users_data import users
from src.models.user_model import User


def get_all():
    return users

def get_by_id(id: int):
    for user in users:
        if user["id"] == id:
            return user

    raise HTTPException(status_code=404, detail=f"Usuario con id {id} no encontrada")

def create_user(user: User):
    users.append(user.model_dump())
    return users

def update_user(id: int, user: User):
    idx = next((i for i, m in enumerate(users) if m["id"] == id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no encontrada")
    
    users[idx] = user.model_dump()

    return users

def delete_by_id(id: int):
    idx = next((i for i, m in enumerate(users) if m["id"] == id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no encontrada")
    
    users.pop(idx)
    return users
    