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