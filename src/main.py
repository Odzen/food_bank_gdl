from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from src.routes import (
    users, auth
)

import os

stage = os.environ.get('stage', None)

print("STAGE: ", stage)

title = f"Food bank API -- {stage}"

app = FastAPI(title=title)

app.include_router(auth.router)
app.include_router(users.router)

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