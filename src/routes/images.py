from src.permissions.users import get_user_from_access_token, user_is_dev
from src.schemas.images import ImageRetrieved
from src.services.images import ImageService
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from src.models import PyObjectId

router = APIRouter()

@router.get("/images/{id}", response_model = ImageRetrieved, tags=["images"],
            dependencies=[Depends(user_is_dev)],
            description="Endpoint that gets an specific image by its id")
async def retrieve_image_by_ID(id: PyObjectId):
    image = ImageService().get_image_by_ID(id)

    return JSONResponse(
        content = jsonable_encoder(image),
        status_code = status.HTTP_200_OK
    )

@router.post("/images", response_model=List[ImageRetrieved], tags=["images"],
    dependencies = [Depends(user_is_dev)],
    description="Endpoint that uploads one or more images to the cloud media storage",
)
async def upload_images(images: List[UploadFile]):
    uploaded_images = await ImageService().upload_images(images)

    return JSONResponse(
        content = jsonable_encoder(uploaded_images),
        status_code = status.HTTP_201_CREATED
    )