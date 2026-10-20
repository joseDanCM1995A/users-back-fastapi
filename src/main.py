

from fastapi import FastAPI

from src.routers.user_router import user_router
from src.routers.basic_auth_router import auth_router
from src.routers.user_router_db import user_router_db


app = FastAPI()

@app.get("/")
def greets() -> dict:
    return {"msg": "hellow world"}

app.include_router(prefix="/users", router = user_router)
app.include_router(prefix="/auth", router = auth_router)
app.include_router(prefix="/usersdb", router = user_router_db)