from fastapi import APIRouter
from app.routers.dependencies.userManager import fastapi_users, auth_backend, get_jwt_strategy
from app.routers.dependencies.oauth import google_oauth_client
from fastapi import Depends, Response
from fastapi_users.authentication import JWTStrategy
import os
from app.schemas.user import UserRead, UserCreate

router = APIRouter()

router.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/jwt", tags=["auth"])
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate), tags=["auth"])
router.include_router(fastapi_users.get_verify_router(UserRead), tags=["auth"])
router.include_router(fastapi_users.get_reset_password_router(), tags=["auth"], )


@router.post("/jwt/refresh")
async def refresh_jwt(response: Response, jwt_strategy: JWTStrategy = Depends(get_jwt_strategy),
                      user=Depends(fastapi_users.current_user(active=True))):
    return await auth_backend.login(jwt_strategy, user, response)

# OAuth Google Existing account association
router.include_router(
    router=fastapi_users.get_oauth_router(
        oauth_client=google_oauth_client,
        backend=auth_backend,
        state_secret=os.getenv("SECRET"),
        associate_by_email=True,
        redirect_url=f"{os.getenv('FRONT_URL')}/auth/associate/google/callback"
    ),
    prefix="/associate/google",
    tags=["auth"]
)

# OAuth Google Association router for authenticated users
router.include_router(
    router=fastapi_users.get_oauth_associate_router(
        oauth_client=google_oauth_client,
        user_schema=UserRead,
        state_secret=os.getenv("SECRET"),
        redirect_url=f"{os.getenv('FRONT_URL')}/auth/associate/google/callback"),
    prefix="/associate-connected/google",
    tags=["auth"]
)

# OAuth google
router.include_router(
    router=fastapi_users.get_oauth_router(
        oauth_client=google_oauth_client,
        backend=auth_backend,
        state_secret=os.getenv("SECRET"),
        redirect_url=f"{os.getenv('FRONT_URL')}/auth/associate/google/callback"
    ),
    prefix="/google",
    tags=["auth"]
)