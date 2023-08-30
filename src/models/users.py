from src.models import PyObjectId
from bson import ObjectId
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class Roles(str, Enum):
    employee = "employee"
    admin  = "admin"
    developer = "developer"

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_name: str
    last_name: str
    email: EmailStr
    role: Roles
    identification: str
    password: str
    created_by: Optional[PyObjectId] | None = None

    last_login: datetime
    created_at: datetime
    updated_at: datetime
    # TODO[pydantic]: The following keys were removed: `json_encoders`.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str}, json_schema_extra={
        "example": {
            "_id": "6adjq9q39dsf214",
            "first_name": "Harry",
            "last_name": "Potter",
            "email": "harry@hogwarts.com",
            "role": "employee",
            "identification": "42156288",
            "password": "99f2a77ff9c6967e8304f6c635a3ed67",
            "created_at": "2023-01-10T18:16:44.595096",
            "updated_at": "2023-01-10T18:16:44.595096"
        }
    })
