from src.schemas.requests import RequestRetrieved, UpdateRequest
from src.services.requests import RequestsService
from fastapi import APIRouter, Body, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from fastapi_pagination import Page, paginate
from src.models import PyObjectId

from src.permissions.users import get_user_from_access_token, user_is_dev, get_optional_user_from_access_token

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

@router.post("/requests/auth", response_model = RequestRetrieved, tags=["requests"])
async def auth_request(email: EmailStr = Body(embed=True)):
    
    request = await RequestsService().auth_request(email)

    return JSONResponse(
        content = jsonable_encoder(request),
        status_code = status.HTTP_200_OK
    )
    
@router.patch("/requests/{request_id}", response_model = RequestRetrieved, tags = ["request"])
async def update_request_by_ID(request_id: PyObjectId, user_requesting=Depends(get_user_from_access_token), updated_request: UpdateRequest = Body()):
    
    updated_request = RequestsService().update_request_by_ID(request_id, updated_request, user_requesting)

    return JSONResponse(
        content=jsonable_encoder(updated_request),
        status_code=status.HTTP_200_OK
    )