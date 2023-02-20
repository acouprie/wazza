from fastapi import Depends, FastAPI

from app.databases.postgres import User, create_db_and_tables
from app.api.dependencies.userManager import auth_backend, current_active_user, fastapi_users
from app.api.auth import router as auth_router
from app.api.users import router as users_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()