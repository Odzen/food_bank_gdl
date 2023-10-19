
from src.services.requests import RequestsService
from src.services.users import UserService
from src.services.tickets import TicketsService
from src.seed.mock import (
    users_for_creation, tickets_for_creation, requests_for_creation
) 
import asyncio


def _generate_mock_users() -> int:
    
    created_users = []
    
    for user in users_for_creation:
        try:
            created_user = UserService().create(user)
            created_users.append(created_user)
        except Exception as e:
            print(e)
            print("Error while creating mock user: " + str(e))
            continue
        
    return len(created_users)

async def _generate_mock_requests() -> int:
    
    created_requests = []
    
    for request in requests_for_creation:
        try:
            created_request = await RequestsService().create_request(request)
            created_requests.append(created_request)
        except Exception as e:
            print("Error while creating mock request: " + str(e))
            continue
         
    return len(created_requests)
        


async def _generate_mock_tickets():
    
    created_tickets = []
    
    for ticket in tickets_for_creation:
        try:
            created_ticket = await TicketsService().create_ticket(ticket)
            created_tickets.append(created_ticket)
        except Exception as e:
            print("Error while creating mock ticket: " + str(e))
            continue
         
    return len(created_tickets)


async def generate_seed_mock_data() -> dict:
    
    response = {}
    
    # first need to run requests before users
    # because users need to be created by an approved request
    
    try:
        qty_requests =  await _generate_mock_requests()
        response["created_requests"] = qty_requests
    except Exception as e:
        print("Error while generating mock requests: " + str(e))
        
    try:
        qty_users = _generate_mock_users()
        response["created_users"] = qty_users
    except Exception as e:
        print("Error while generating mock users: " + str(e))
        
    try:
        qty_tickets = await _generate_mock_tickets()
        response["created_tickets"] = qty_tickets
    except Exception as e:
        print("Error while generating mock tickets: " + str(e))
        
    return response

async def main():
    data = await generate_seed_mock_data()
    print("Created Data: ", data)

asyncio.run(main())
    
    