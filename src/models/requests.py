from src.models import PyObjectId
from bson import ObjectId
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class TypeRequest(str, Enum):
    authorization = "authorization"
    account_creation  = "account_creation"
    other = "other"

class StateRequest(str, Enum):
    pending = "pending"
    approved  = "approved"
    stand_by = "stand_by"
    rejected = "rejected"
    
class Request(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    type: TypeRequest
    email: Optional[EmailStr]
    state: StateRequest
    title: Optional[str]
    description: Optional[str]
    
    created_by: Optional[PyObjectId] | None = None
    proccessed_by: Optional[PyObjectId] | None = None
    
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str}, json_schema_extra={
        "example": {
            "_id": "6adjq9q39dsf214",
            "type": "account_creation",
            "state": "pending",
            "title": "Account creation for juan@mail.com",
            "description": "juan@mail.com wants to create an account",
            "created_by": "None",
            "proccessed_by": "6adjq9q39dsf214",
            "created_at": "2023-01-10T18:16:44.595096",
            "updated_at": "2023-01-10T18:16:44.595096"
        }
    })