from pydantic import BaseModel
from pydantic import BaseModel, EmailStr
from enum import Enum

class AvailableTemplatesNames(str, Enum):
    auth_request = "auth-request"
    notification_user_auth = "notification-user-auth"
    notify_tickets = "notify-tickets"

class SendEmailBody(BaseModel):
    recipient_name: str
    recipient_email: EmailStr
    subject: str
    template: AvailableTemplatesNames
    variables: dict
    
class ResponseEmailSent(BaseModel):
    id: str
    message: str