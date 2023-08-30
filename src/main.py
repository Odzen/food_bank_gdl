from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from src.routes import (
    auth, users
)

import os
# from config import stage

# Setting up path that is used to server the app
# To make it work live on AWS Lambda and locally

stage = os.environ.get('stage', None)

prefix = f"/{stage}" if stage else "/"

print("STAGE: ", stage)
print("prefix: ", prefix)

title = f"Food bank API -- {stage}"

app = FastAPI(title=title, root_path=prefix)

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