from src.models.users import Roles, User
from bson import ObjectId
from datetime import datetime
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class CreateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    role: Roles = Field(default=Roles.employee)
    identification: str
    password: str

    last_login: datetime = Field(default_factory = datetime.now)
    created_at: datetime = Field(default_factory = datetime.now)
    updated_at: datetime = Field(default_factory = datetime.now)

    class config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        fields = {'id': '_id'}
        json_schema_extra = {
                "example": {
                    "first_name": "Harry",
                    "last_name": "Potter",
                    "email": "harry@hogwarts.com",
                    "role": "employee",
                    "identification": "42156288",
                    "password": "99f2a77ff9c6967e8304f6c635a3ed67",
                    "created_at": "2023-01-10T18:16:44.595096",
                    "updated_at": "2023-01-10T18:16:44.595096"
            }
        }

class UserRetrieved(User):
    model_config = ConfigDict(exclude={'password'})
    
    
class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Roles] = None
    identification: Optional[str] = None
    
    updated_at: datetime = Field(default_factory = datetime.now)
    model_config = ConfigDict(populate_by_name=True, json_encoders={ObjectId: str})