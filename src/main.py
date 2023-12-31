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

app = FastAPI(title=title)

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