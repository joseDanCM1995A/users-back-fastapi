from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.store.users_data import users_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 5
SECRET = "280295A"

class User(BaseModel):
    name: str
    username: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
auth_router = APIRouter()
crypt = CryptContext(schemes=["bcrypt"])


def user_authenticated(token: str = Depends(oauth2)):
    exception_custom = HTTPException(
            status_code=401,
            detail="credenciales de autenticacion invalidas",
            headers={"WWW-Autenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")


        if username is None:
            raise exception_custom
        
    except JWTError:
        raise exception_custom

    return search(username)
 

def current_user(user: User = Depends(user_authenticated)):

    if user.disabled:
        raise HTTPException(status_code=400, detail=f"usuario inactivo", headers={"WWW-Autenticate": "Bearer"})
 
    return user

def search_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search(username: str):
    if username in users_db:
        return User(**users_db[username])

@auth_router.post('/login', tags=["auth"])
def login(form: OAuth2PasswordRequestForm = Depends()):
    userdb = users_db.get(form.username) # solo busca que exista el usuario en la data
    
    if not userdb:
        raise HTTPException(status_code=400, detail=f"Usuario incorrecto")
        
    user = search_db(form.username) #trea el dato ya con password

    if crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail=f"contrasena incorrecto")

    access_token = {
        "sub": user.username,
        "exp":  datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION),
    }

    return {"acces_token":jwt.encode(access_token, SECRET, algorithm=ALGORITHM) , "token_type": "bearer"}
         


@auth_router.get('/me', tags=["auth"])
def search_by_username(username: User = Depends(current_user)):
    return username
    

