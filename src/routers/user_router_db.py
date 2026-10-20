from fastapi import APIRouter, Path, status
from src.services.user_service import get_all, get_by_id, update_user, create_user, delete_by_id
from src.config.db.models.userdb import Userdb
from typing import List, Optional

user_router_db = APIRouter()

@user_router_db.get('/', tags=['usersdb'], status_code=status.HTTP_200_OK)
def user(page: Optional[int] = None, limit: Optional[int] = None) -> List[Userdb]:
    return get_all()

@user_router_db.get('/{id}', tags=['usersdb'], status_code=status.HTTP_200_OK)
def user_by_id(id: str):
    return get_by_id(id)

@user_router_db.post('/', tags=['usersdb'], status_code=status.HTTP_201_CREATED)
def c_user(newUser: Userdb):
    return create_user(newUser)

@user_router_db.put('/', tags=['usersdb'], status_code=status.HTTP_200_OK)
def u_user(userUpdated: Userdb):
    return update_user(userUpdated)

@user_router_db.delete('/{id}', tags=['usersdb'], status_code=status.HTTP_200_OK)
def d_user(id: str):
    return delete_by_id(id) 