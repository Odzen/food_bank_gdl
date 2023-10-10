from src.models import PyObjectId
from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class Image(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    url: str
    content_type: str
    size: float
    uploaded: bool
    date_uploaded: datetime

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str}, json_schema_extra={
        "example": {
            "_id": "6adjq9q39dsf214",
            "name": "image123",
            "url": "https://image123.s3.aws.com",
            "content_type": "image/png",
            "size": 2418241,
            "uploaded": True,
            "date_uploaded": "2032-04-23T10:20:30"
        }
    })
        


class NestedImage(BaseModel):
    uploaded_image_id: PyObjectId | int
    url: str
    content_type: str = Field(default = "image")

    model_config =  ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str}, json_schema_extra={
        "example": {
            "_id": "64bda5b3c5962cdbe3362255",
            "url": "https://macondo-tokenization-images-dev.s3.amazonaws.com/64bda5b3c5962cdbe3362255.png",
            "content_type": "image/png",
        }
    })