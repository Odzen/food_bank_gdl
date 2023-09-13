from pydantic import BaseModel
from pydantic import BaseModel, EmailStr
from enum import Enum

class AvailableTemplatesNames(str, Enum):
    auth_request = "auth-request"

class SendEmailBody(BaseModel):
    recipient_name: str
    recipient_email: EmailStr
    subject: str
    template: AvailableTemplatesNames
    variables: dict
    
class ResponseEmailSent(BaseModel):
    id: str
    message: str