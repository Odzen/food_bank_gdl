from src.models.images import Image
from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import ConfigDict

class FolderImages(str, Enum):
    profile_pictures = "tickets_pictures"
    none = None

class ImageRetrieved(Image):
    pass

class UpdateImage():
    name: Optional[str]
    url: Optional[str]
    content_type: Optional[str]
    size: Optional[bytes]
    uploaded: Optional[bool]
    date_uploaded: Optional[datetime]

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_schema_extra={

            "example": {
                "name": "image123",
                "url": "https://image123.s3.aws.com",
                "content_typ": "image/png",
                "size": 2418241,
                "uploaded": True,
                "date_uploaded": "2032-04-23T10:20:30"
            }
        }
    )