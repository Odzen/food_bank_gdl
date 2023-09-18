from src.schemas.users import UserRetrieved, UpdateUser, CreateUser
from src.services.users import UserService, Roles
from fastapi import APIRouter, Body, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, paginate
from pydantic import EmailStr
from src.models import PyObjectId
from src.permissions.users import user_roles_checks, get_user_from_access_token, user_is_dev, get_optional_user_from_access_token

router = APIRouter()


@router.get("/users/{id}", response_model=UserRetrieved, tags=["users"])
async def retrieve_user_by_id(id: PyObjectId, user=Depends(user_is_dev)):
    
    user = UserService().get_user_by_ID(id)
    user_json = jsonable_encoder(user)

    user = UserRetrieved(**user_json)

    return JSONResponse(
        content=jsonable_encoder(user),
        status_code=status.HTTP_200_OK
    )


@router.get("/users", response_model=Page[dict], dependencies=[Depends(get_user_from_access_token)], tags=["users"])
async def list_all_users(email: EmailStr = None, role: Roles = None):
    users = []

    if email:
        users = [
            UserService().get_user_by_email(email)
        ]
    else:
        users = UserService().list_all_users(role=role)

    return paginate(
        jsonable_encoder(users)
    )
    
@router.patch("/users/{user_id}", response_model = UserRetrieved, tags = ["users"])
async def update_user_by_ID(user_id: PyObjectId, user=Depends(get_user_from_access_token), user_to_patch: UpdateUser = Body()):
    
    user_roles_checks(user_action=user_to_patch, user=user)
    
    user = UserService().update_user_by_ID(user_id, user_to_patch)

    return JSONResponse(
        content=jsonable_encoder(user),
        status_code=status.HTTP_200_OK
    )
    
@router.post("/users", response_model=UserRetrieved, tags=["auth"])
async def signup(user=Depends(get_optional_user_from_access_token), user_to_create: CreateUser = Body()):

    if user:
        user_roles_checks(user_action=user_to_create, user=user)
    
        user = UserService().create(user_to_create=user_to_create, user_id_creator=user.id)

    user = UserService().create(user_to_create=user_to_create)
    
    user_json = jsonable_encoder(user)
    user = UserRetrieved(**user_json)

    return JSONResponse(
        content = {
            "user": jsonable_encoder(user)
        },
        status_code = status.HTTP_201_CREATED
    )