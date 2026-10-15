

from fastapi import FastAPI

from src.routers.user_router import user_router


app = FastAPI()

@app.get("/")
def greets() -> dict:
    return {"msg": "hellow world"}

app.include_router(prefix="/users", router = user_router)