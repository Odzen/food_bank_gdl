from src.config.db import db
from fastapi import HTTPException, status
from pydantic import EmailStr
from src.schemas.requests import RequestRetrieved, CreateRequest, UpdateRequest
from src.models.requests import TypeRequest, StateRequest
from typing import List
from src.services.mailgun import MailgunService
from pymongo import ReturnDocument
from src.models import PyObjectId
from src.schemas.mailgun import SendEmailBody, AvailableTemplatesNames
from fastapi.encoders import jsonable_encoder
from src.services.users import UserService
from src.schemas.users import Roles
from src.models.users import User

class RequestsService():
    
    def __init__(self):
        self.requests_collection = db["requests"]
        
        
    async def list_all_requests(self) -> List[RequestRetrieved]:
        requests = []
        
        requests_found = self.requests_collection.find()
        
        for request_document in requests_found:
            requests.append(RequestRetrieved(**request_document))
            
        return requests
    
    async def get_request_by_ID(self, id: PyObjectId) -> RequestRetrieved:
        request = self.requests_collection.find_one({"_id": id})

        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request doesn't exist. Wrong ID."
            )

        return RequestRetrieved(**request) 
    
    async def create_request(self, request_to_create: CreateRequest) -> RequestRetrieved:
        try:
            request_to_create = jsonable_encoder(request_to_create)
            inserted_request = self.requests_collection.insert_one(request_to_create)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Error while creating the request: " + str(e)
            )

        request_id = inserted_request.inserted_id
        
        request = await self.get_request_by_ID(request_id)

        return request

    
    async def auth_request(self, email: EmailStr) -> RequestRetrieved:
        
        existing_request = self.requests_collection.find_one({"email": email, "type": TypeRequest.account_creation})
        
        if existing_request and existing_request["state"] == StateRequest.pending:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="There is a pending request with this email."
            )

        if existing_request and existing_request["state"] == StateRequest.approved:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="There is a approved request with this email."
            )  
        
        request_to_create = CreateRequest(
            type = TypeRequest.account_creation,
            state = StateRequest.pending,
            email = email,
            title = "Account creation for " + email,
            description = email + " wants to create an account"
        )
        
        created_request = await self.create_request(request_to_create)
        
        if not created_request:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Could not create the request."
            )
        
        # Send email to notify the admins
        admins = UserService().list_all_users(role=Roles.admin)

        for admin in admins:
            recipient_name = admin.first_name + " " + admin.last_name
            recipient_email = admin.email
            subject = "Solicitud de creación de cuenta"
            template = AvailableTemplatesNames.auth_request
            variables = {
                "email-request-creation": email
            }
            
            email_to_send = SendEmailBody(
                recipient_name = recipient_name,
                recipient_email = recipient_email,
                subject = subject,
                template = template,
                variables = variables
            )
            
            MailgunService().send_template_email(email_to_send)
        
        
        return created_request
    
    async def update_request_by_ID(self, id: PyObjectId, update_request: UpdateRequest, user_requesting: User) -> RequestRetrieved:
        #If the user is admin
        # if request is account_creation
        # send email to the user requesting the account creation
        
        return
        