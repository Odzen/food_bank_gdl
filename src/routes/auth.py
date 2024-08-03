from pydantic import EmailStr
from src.schemas.users import UserRetrieved, User
from src.services.auth import AuthService
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.permissions.users import get_user_from_access_token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


router = APIRouter()

@router.post("/login", response_model = UserRetrieved, tags=["auth"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    username = form_data.username
    password = form_data.password
    
    user, access_token = AuthService().login(username, password)
    user_json = jsonable_encoder(user)
    user = UserRetrieved(**user_json)

    return JSONResponse(
        content = {
            "user": jsonable_encoder(user),
            "access_token": access_token,
            "type": "bearer"
        },
        status_code = status.HTTP_200_OK
    )

@router.get("/me", response_model = UserRetrieved, tags=["auth"])
async def retrieve_user_by_access_token(user_from_token: User = Depends(get_user_from_access_token)):
    return user_from_token

