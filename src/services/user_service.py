from typing import List

from fastapi import HTTPException, status

from src.store.users_data import users
from src.config.db.models.userdb import Userdb
from src.config.db.schemas.user import user_schema, users_schema

from src.config.client import db
from bson import ObjectId

def get_all() -> List[Userdb]:
    return users_schema(db.local.users.find())

def get_by_id(id: str):
    return search_user("_id", ObjectId(id))

def create_user(user: Userdb):
    #valida si existe el usuario y lo valida que sea un Usuario tipo User
    if type(search_user("email", user.email)) == Userdb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ya existe un usuario con email {user.email}")
        

    #comnvertimos en un diccionario al user que recibimos
    user_dic = dict(user)

    #eliminar el id cuando se inserta, no es necesario y e impd9imos que se vaya en null en la insercion
    del user_dic['id'] 

    #bucando el nuevo registro
    id = db.local.users.insert_one(user_dic).inserted_id

    # se parsea a lo que queremos que regrese
    new_user = user_schema(db.local.users.find_one({"_id": id}))

    return Userdb(**new_user)

def update_user(user: Userdb):
    user_dict = dict(user)
    del user_dict['id']

    try: 
        db.local.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha podidio actualizar el usuario"}

    return search_user("_id", ObjectId(user.id))

def delete_by_id(id: str):
    user_found = db.local.users.find_one_and_delete({"_id": ObjectId(id)})

    if not user_found:
        return {"error": "No se ha eliminado el usuario"}
    

def search_user(field: str, key): # el key es generico, puede llegarle cualquier tipo
    try:
        user = db.local.users.find_one({field: key})
        return Userdb(**user_schema(user))
    except:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario no encontrado")
        return {"error": "No se ha encontrado el usuario"}