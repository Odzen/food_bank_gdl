from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from src.models import PyObjectId
from datetime import datetime
from typing import Optional
from bson import ObjectId

class UrgencyTicketEnum(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"
    
class StateTicketEnum(str, Enum):
    pending = "pending"
    authorization = "authorization"
    in_progress = "in_progress"
    blocked = "blocked"
    resolved = "resolved"

class Ticket(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: Optional[str]
    
    urgency: UrgencyTicketEnum
    state: StateTicketEnum
    
    created_by: PyObjectId
    assigned_to: Optional[PyObjectId] | None = None
    
    time_solved: Optional[datetime]

    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str}, json_schema_extra={
        "example": {
            "_id": "6adjq9q39dsf211",
            "title:": "No enough food",
            "description": "We need more food",
            "urgency": "high",
            "state": "pending",
            "created_by": "6adjq9q39dsf212",
            "assigned_to": "6adjq9q39dsf211",
            "time_solved": "2023-01-10T18:16:44.595092",
            "created_at": "2023-01-10T18:16:44.595096",
            "updated_at": "2023-01-10T18:16:44.595096"
        }
    })
    
    