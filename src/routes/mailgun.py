
from fastapi import APIRouter, Body, status, Depends
from src.services.mailgun import MailgunService
from fastapi.responses import JSONResponse
from src.schemas.mailgun import SendEmailBody
from src.permissions.users import user_is_dev

router = APIRouter()
@router.post("/mailgun", response_model=dict, tags=["mailgun"], dependencies=[Depends(user_is_dev)])
async def send_template_email(send_email_body : SendEmailBody = Body()):
    
    response = await MailgunService().send_template_email(send_email_body)
    
    return JSONResponse(
        content = response,
        status_code = status.HTTP_200_OK
    )