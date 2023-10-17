from src.config.db import db
from fastapi import HTTPException, status, UploadFile
from typing import List
from src.schemas.tickets import TicketRetrieved, CreateTicket, UpdateTicket
from src.models import PyObjectId
from src.models.users import User, Roles
from fastapi.encoders import jsonable_encoder
from src.services.users import UserService
from pymongo import ReturnDocument
from src.services.mailgun import MailgunService
from src.schemas.images import FolderImages
from src.services.images import ImageService
from src.schemas.mailgun import AvailableTemplatesNames, SendEmailBody, ResponseEmailSent

class TicketsService():
    def __init__(self):
        self.tickets_collection = db["tickets"]
        
    async def list_all_tickets(self) -> List[TicketRetrieved]:
        tickets = []
        
        tickets_found = self.tickets_collection.find()
        
        for ticket_document in tickets_found:
            tickets.append(TicketRetrieved(**ticket_document))
            
        return tickets
    
    
    async def get_ticket_by_Id(self, id: PyObjectId) -> TicketRetrieved:
        ticket = self.tickets_collection.find_one({"_id": id})

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket doesn't exist. Wrong ID."
            )

        return TicketRetrieved(**ticket) 
    
    
    async def create_ticket(self, ticket_to_create: CreateTicket, user_creator: User = None) -> TicketRetrieved:
        try:
            ticket_to_create = jsonable_encoder(ticket_to_create)
            inserted_ticket = self.tickets_collection.insert_one(ticket_to_create)
            
            if user_creator:
                self.tickets_collection.find_one_and_update(
                    {"_id": inserted_ticket.inserted_id},
                    {"$set": {"created_by": user_creator.id}},
                    return_document= ReturnDocument.AFTER
                )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Error while creating the ticket: " + str(e)
            )

        ticket_id = inserted_ticket.inserted_id
        
        ticket = await self.get_ticket_by_Id(ticket_id)
        
        # Send notification by email
        if ticket.assigned_to:
            user_assigned = UserService().get_user_by_ID(ticket.assigned_to)
            
            self._send_email_to_assigned_user(user_assigned.email, user_assigned.first_name, ticket.title)

        return ticket
    
    async def update_ticket_by_Id(self, id: PyObjectId, update_ticket: UpdateTicket, user_requesting: User) -> TicketRetrieved:
        
        current_ticket = await self.get_ticket_by_Id(id)
        
        if user_requesting.role == Roles.employee and (current_ticket.assigned_to != user_requesting.id or current_ticket.created_by != user_requesting.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Employees are allowed to update only the tickets that they own or the ones that they're assigned to."
            )
        
        updated_ticket_dict = jsonable_encoder(update_ticket, exclude_none = True)
       
        updated_ticket = self.tickets_collection.find_one_and_update(
            {"_id": id},
            {"$set": updated_ticket_dict},
            return_document=ReturnDocument.AFTER
        )
        
        if not updated_ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket doesn't exist. Wrong ID."
            )
            
        ticket_retrieved = TicketRetrieved(**updated_ticket)
        
        # Send notification by email
        if ticket_retrieved.assigned_to:
            user_assigned = UserService().get_user_by_ID(ticket_retrieved.assigned_to)
            
            self._send_email_to_assigned_user(user_assigned.email, user_assigned.first_name, ticket_retrieved.title)
        
        return ticket_retrieved
    
    def _send_email_to_assigned_user(self, user_email: str, user_name: str, title_ticket: str) -> ResponseEmailSent:

            subject = "¡Haz sido asignado a un ticket!"
            template = AvailableTemplatesNames.notify_tickets
            variables = {
                "name": user_name,
                "title": title_ticket
            }
            
            email_to_send = SendEmailBody(
                recipient_name = user_name,
                recipient_email = user_email,
                subject = subject,
                template = template,
                variables = variables
            )
            
            print("Email to send: ", email_to_send)
            
            response = MailgunService().send_template_email(email_to_send)
            
            print("Response: ", response)
            
            return response
    

    async def upload_ticket_images(self, ticket_images: List[UploadFile],   ticket_id: PyObjectId) -> TicketRetrieved:
        new_ticket_images = await ImageService().upload_images(images=ticket_images, folder=FolderImages.tickets_pictures)

        for new_ticket_image in new_ticket_images:
    
            new_image_data = {
                "uploaded_image_id": new_ticket_image.id,
                "url": new_ticket_image.url,
                "content_type": new_ticket_image.content_type
            }
            
            updated_ticket = self.tickets_collection.find_one_and_update(
                {"_id": ticket_id},
                {"$push": {"images": new_image_data}},
                return_document=ReturnDocument.AFTER
            )
            
            if not updated_ticket:
                raise HTTPException(
                    detail=f"Ticket with the id={ticket_id} doesn't exist",
                    status_code=status.HTTP_409_CONFLICT
                )
        
        return TicketRetrieved(**updated_ticket)
    