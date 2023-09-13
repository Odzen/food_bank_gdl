from bson import ObjectId
from datetime import datetime
from pydantic import ConfigDict, BaseModel, Field
from typing import Optional
from datetime import datetime
from src.models.requests import TypeRequest, StateRequest, Request

class CreateRequest(BaseModel):
    type: TypeRequest
    state: StateRequest
    title: Optional[str]
    description: Optional[str]
    
    created_at: datetime = Field(default_factory = datetime.now)
    updated_at: datetime = Field(default_factory = datetime.now)
    
    model_config = ConfigDict(
        populate_by_name=True, 
        arbitrary_types_allowed=True, 
        json_encoders={ObjectId: str},
        fields = {'id': '_id'},
        json_schema_extra={
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
    
class RequestRetrieved(Request):
    pass

class UpdateRequest(BaseModel):
    type: Optional[TypeRequest] = None
    state: Optional[StateRequest] = None
    title: Optional[str] = None
    description: Optional[str] = None
    
    updated_at: datetime = Field(default_factory = datetime.now)
    model_config = ConfigDict(populate_by_name=True, json_encoders={ObjectId: str})