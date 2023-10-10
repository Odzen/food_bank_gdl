from src.config.aws import images_bucket_name, s3_client
from src.config.db import db
from src.models import PyObjectId
from src.models.images import Image, NestedImage
from src.schemas.images import UpdateImage, FolderImages
from botocore.exceptions import ClientError
from bson import ObjectId
from datetime import datetime
from fastapi import UploadFile, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import ReturnDocument
from typing import List


class ImageService():

    def __init__(self):
        self.images_collection = db["images"]
        self.s3_client = s3_client
        self.bucket_name = images_bucket_name

    def get_image_by_ID(self, id: str) -> Image:
        id = ObjectId(id)
        image = self.images_collection.find_one({"_id": id})

        if not image:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Image doesn't exist. Wrong ID."
            )
        
        return Image(**image)

    def _get_nested_image_by_id(self, id: PyObjectId) -> NestedImage:
        image = self.images_collection.find_one({"_id": id})

        if not image:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Image doesn't exist. Wrong ID."
            )

        image["uploaded_image_id"] = image["_id"]
        del image["_id"]

        return NestedImage(**image)

    def _update_image_by_ID(self, id: str, image: UpdateImage) -> Image:
        id = ObjectId(id)
        image_to_update_dict = jsonable_encoder(image)
        
        updated_image = self.images_collection.find_one_and_update(
            {"_id": id},
            {"$set": image_to_update_dict},
            return_document = ReturnDocument.AFTER
        )

        return Image(**updated_image)

    async def upload_images(self, images: List[UploadFile], folder: FolderImages = FolderImages.none) -> List[Image]:
        uploaded_images = []

        for image in images:
            image_readed = await image.read()            

            try:
                new_image = self.images_collection.insert_one({
                    "name": None,
                    "url": None,
                    "content_type": image.content_type,
                    "size": len(image_readed),
                    "uploaded": False,
                    "date_uploaded": None,
                })

                new_image_id = new_image.inserted_id
                image_extension = image.filename.split(".")[-1]
                image_name = f"{new_image_id}.{image_extension}"

                image_key = f"{image_name}"
                
                if folder != FolderImages.none:
                    image_key = f"{folder}/{image_key}"

                self.s3_client.put_object(
                    Body = image_readed,
                    Bucket = self.bucket_name,
                    Key = image_key
                )
                
                uploaded_image_url = self.s3_client.generate_presigned_url(
                    "get_object",
                    Params = {"Bucket": self.bucket_name, "Key": image_key}
                )
                uploaded_image_url = uploaded_image_url.split("?")[0]

                uploaded_image = self._update_image_by_ID(new_image_id, {
                    "name": image_name,
                    "url": uploaded_image_url,
                    "uploaded": True,
                    "date_uploaded": datetime.now()
                })

                uploaded_images.append(uploaded_image)

            except (ClientError, AttributeError) as e:
                print(e)
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = "An error has ocurred uploading the image. Please try later."
                )
            
        return uploaded_images
            