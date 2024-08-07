from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from fastapi.testclient import TestClient

from src.routes import (
    users, auth, mailgun, requests, tickets, images
)

import os

stage = os.getenv("stage", "dev")

print("STAGE: ", stage)

title = f"Food bank API -- {stage}"

description = """
Food bank API helps you to perform administrative tasks for the [Food Bank - Guadalajara](https://bdalimentos.org/).
The API can be used for other food banks as well, or any other organization that shares similar needs.

## Users

Developer users can:

* **CRUD** operations on all entities.
* Send template emails using [Mailgun](https://www.mailgun.com/).
* Upload images to the cloud media storage and get them by ID. Using direct endpoints.

Admin users can:
* **CRUD** operations on all Requests, tickets, other administrators or employees.

Employees can:
* Create requests, modify and read request created by them.
* Create tickets, modify and read tickets created by them.

All users can:
* Request an account creation to admin users. (A user can't create an account without admin approval)

## Requests

A request is a petition to be approved or rejected. It has a type, status, title, description and other relevant fields.
The requests are created by employees, for the admin users to approve or reject them.

## Tickets

A ticket is a task to be done. It has a urgency level, status, associated images and other relevant fields.
Usually the tickets are created by employees, but can be created by admin users as well.
The ticket could be assigned to a user, if so, the user will receive an email notification, because the task should be completed by him/her before a deadline.
"""


app = FastAPI(
    title=title,
    description=description,
    version="0.1",
    contact={
        "name": "Juan Sebastian Velasquez",
        "url": "https://github.com/Odzen",
        "email": "jsebastian.va@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

testing_client = TestClient(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(mailgun.router)
app.include_router(requests.router)
app.include_router(tickets.router)
app.include_router(images.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

add_pagination(app)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to Food Bank API, explore the docs at /docs."}