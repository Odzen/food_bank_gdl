from src.models.tickets import Ticket, StateTicketEnum, UrgencyTicketEnum
from pydantic import BaseModel, Field, ConfigDict
from src.models import PyObjectId
from datetime import datetime
from typing import Optional
from bson import ObjectId

class CreateTicket(BaseModel):
    title: str
    description: Optional[str] = None
    
    urgency: UrgencyTicketEnum
    state: StateTicketEnum = Field(default=StateTicketEnum.pending)
    
    assigned_to: Optional[PyObjectId] | None = None

    created_at: datetime = Field(default_factory = datetime.now)
    updated_at: datetime = Field(default_factory = datetime.now)
    
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

class TicketRetrieved(Ticket):
    pass

class UpdateTicket(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    
    urgency: Optional[UrgencyTicketEnum] = None
    state: Optional[StateTicketEnum] = None
    
    assigned_to: Optional[PyObjectId]= None
    
    updated_at: datetime = Field(default_factory = datetime.now)
    
    model_config = ConfigDict(populate_by_name=True, json_encoders={ObjectId: str})