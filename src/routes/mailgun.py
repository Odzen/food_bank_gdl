
from fastapi import APIRouter, Body, status, Depends
from src.services.mailgun import MailgunService
from fastapi.responses import JSONResponse
from src.schemas.mailgun import SendEmailBody, ResponseEmailSent
from src.permissions.users import user_is_dev
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/mailgun", response_model=ResponseEmailSent, tags=["mailgun"], dependencies=[Depends(user_is_dev)])
def send_template_email(send_email_body : SendEmailBody = Body()):
    
    response = MailgunService().send_template_email(send_email_body)
    
    return JSONResponse(
        content = jsonable_encoder(response),
        status_code = status.HTTP_200_OK
    )