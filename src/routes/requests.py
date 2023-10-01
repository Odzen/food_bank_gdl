from src.schemas.requests import RequestRetrieved, UpdateRequest, CreateRequest, TypeRequest
from src.services.requests import RequestsService
from fastapi import APIRouter, Body, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from fastapi_pagination import Page, paginate
from src.models import PyObjectId
from src.models.users import User
from src.permissions.users import get_user_from_access_token, user_is_admin_or_dev

router = APIRouter()

@router.get("/requests/{id}", response_model=RequestRetrieved, tags=["requests"])
async def retrieve_request_by_id(id: PyObjectId):
    
    request = await RequestsService().get_request_by_ID(id)

    return JSONResponse(
        content=jsonable_encoder(request),
        status_code=status.HTTP_200_OK
    )

@router.get("/requests", response_model = Page[dict], dependencies=[Depends(get_user_from_access_token)], tags=["requests"])
async def get_all_requests():
    
    requests = await RequestsService().list_all_requests()

    return paginate(
        jsonable_encoder(requests)
    )

@router.post("/requests", response_model = RequestRetrieved, tags=["requests"], 
             description="Endpoint to create a request. Any logged user can perform this action. To create any request except account creation's")
async def create_request(request_to_create: CreateRequest = Body(), user: User = Depends(get_user_from_access_token)):

    if request_to_create.type == TypeRequest.account_creation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="To create a account creation request, use /requests/auth endpoint."
        )    
    
    request = await RequestsService().create_request(request_to_create=request_to_create, user_creator=user)

    return JSONResponse(
        content = jsonable_encoder(request),
        status_code = status.HTTP_200_OK
    )

@router.post("/requests/auth", response_model = RequestRetrieved, tags=["requests"],
             description="Endpoint to create a account creation request. Anyone can execute this actions."
             "This endpoint should be called in order to authorize a user to create an account")
async def auth_request(email: EmailStr = Body(embed=True)):
    
    request = await RequestsService().auth_request(email)

    return JSONResponse(
        content = jsonable_encoder(request),
        status_code = status.HTTP_200_OK
    )
    
@router.patch("/requests/{request_id}", response_model = RequestRetrieved, 
              tags = ["request"],
              description="Endpoint to update a request by ID. Only developers and admins can perform this action.")
async def update_request_by_ID(request_id: PyObjectId, user_requesting=Depends(user_is_admin_or_dev), updated_request: UpdateRequest = Body()):
    
    updated_request = await RequestsService().update_request_by_ID(request_id, updated_request, user_requesting)

    return JSONResponse(
        content=jsonable_encoder(updated_request),
        status_code=status.HTTP_200_OK
    )