from bson import ObjectId
from datetime import datetime
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from src.models.requests import TypeRequest, StateRequest, Request

class CreateRequest(BaseModel):
    type: TypeRequest
    state: StateRequest = Field(default=StateRequest.pending)
    email: Optional[EmailStr] = None
    title: Optional[str] = None
    description: Optional[str] = None
    
    created_at: datetime = Field(default_factory = datetime.now)
    updated_at: datetime = Field(default_factory = datetime.now)
    
    model_config = ConfigDict(
        populate_by_name=True, 
        arbitrary_types_allowed=True, 
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "type": "account_creation",
                "state": "pending",
                "title": "Account creation for juan@mail.com",
                "description": "juan@mail.com wants to create an account"
            }
    })
    
class RequestRetrieved(Request):
    pass

class UpdateRequest(BaseModel):
    type: Optional[TypeRequest] = None
    state: Optional[StateRequest] = None
    title: Optional[str] = None
    description: Optional[str] = None
    
    updated_at: datetime = Field(default_factory = datetime.now)
    model_config = ConfigDict(populate_by_name=True, json_encoders={ObjectId: str})