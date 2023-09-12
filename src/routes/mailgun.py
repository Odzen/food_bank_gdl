
from fastapi import APIRouter, Body, status, Depends
from src.services.mailgun import MailgunService
from fastapi.responses import JSONResponse

router = APIRouter()
@router.post("/mailgun", response_model=dict, tags=["mailgun"])
async def send_template_email(to: str = Body(), subject: str = Body(), template: str = Body(), variables: dict  = Body()):
    
    response = await MailgunService().send_template_email(to, subject, template, variables)
    
    return JSONResponse(
        content = response,
        status_code = status.HTTP_200_OK
    )