from src.schemas.tickets import CreateTicket, TicketRetrieved, UpdateTicket
from src.services.tickets import TicketsService
from fastapi import APIRouter, Body, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from fastapi_pagination import Page, paginate
from src.models import PyObjectId
from src.models.users import User
from src.permissions.users import get_user_from_access_token, user_is_admin_or_dev


router = APIRouter()

@router.get("/tickets/{id}", response_model=TicketRetrieved, tags=["tickets"])
async def retrieve_ticket_by_id(id: PyObjectId):
    
    ticket = await TicketsService().get_ticket_by_Id(id)

    return JSONResponse(
        content=jsonable_encoder(ticket),
        status_code=status.HTTP_200_OK
    )

@router.get("/tickets", response_model = Page[dict], dependencies=[Depends(get_user_from_access_token)], tags=["tickets"])
async def get_all_tickets():
    
    tickets = await TicketsService().list_all_tickets()

    return paginate(
        jsonable_encoder(tickets)
    )

@router.post("/tickets", response_model = TicketRetrieved, tags=["tickets"], 
             description="Endpoint to create a ticket. Any logged user can perform this action.")
async def create_ticket(ticket_to_create: CreateTicket = Body(), user: User = Depends(get_user_from_access_token)):
    
    ticket = await TicketsService().create_ticket(ticket_to_create=ticket_to_create, user_creator=user)

    return JSONResponse(
        content = jsonable_encoder(ticket),
        status_code = status.HTTP_200_OK
    )

    
@router.patch("/tickets/{ticket_id}", response_model = TicketRetrieved, 
              tags = ["ticket"],
              description="Endpoint to update a ticket by ID. Only creators of the ticket can perform this action or admins.")
async def update_ticket_by_Id(ticket_id: PyObjectId, 
                               user_ticketing=Depends(get_user_from_access_token),
                               updated_ticket: UpdateTicket = Body()):
    
    updated_ticket = await TicketsService().update_ticket_by_Id(ticket_id, updated_ticket, user_ticketing)

    return JSONResponse(
        content=jsonable_encoder(updated_ticket),
        status_code=status.HTTP_200_OK
    )