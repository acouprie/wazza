from typing import Union

from app.db import get_conn, close_conn

from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup():
    get_conn(app)

@app.on_event("shutdown")
async def shutdown():
    close_conn(app)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}