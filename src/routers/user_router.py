from fastapi import APIRouter, Path
from src.services.user_service import get_all, get_by_id, update_user, create_user, delete_by_id
from src.models.user_model import User
from typing import List, Optional

user_router = APIRouter()

@user_router.get('/', tags=['users'], status_code=200)
def user(page: Optional[int] = None, limit: Optional[int] = None) -> List[User]:
    return get_all()

@user_router.get('/{id}', tags=['users'], status_code=201)
def user_by_id(id: int = Path(ge=0)) -> User:
    return get_by_id(id)

@user_router.post('/', tags=['users'], status_code=201)
def c_user(newUser: User) -> List[User]:
    return create_user(newUser)

@user_router.put('/{id}', tags=['users'], status_code=200)
def u_user(userUpdated: User, id: int = Path(ge=0)) -> List[User]:
    return update_user(id, userUpdated)

@user_router.delete('/{id}', tags=['users'], status_code=200)
def d_user(id: int = Path(ge=0)) -> List[User]:
    return delete_by_id(id)