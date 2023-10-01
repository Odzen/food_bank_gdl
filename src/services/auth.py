from src.config.db import db
from fastapi import HTTPException, status
from pydantic import EmailStr
from src.models.users import User
from src.utils.cryptography import (
    create_access_token, verify_password
)
from typing import Tuple
from datetime import datetime
from pymongo import ReturnDocument

class AuthService():
    
    def __init__(self):
        self.users_collection = db["users"]
        
    def login(self, email: EmailStr, password: str) -> Tuple[User, str]:
        user = self.users_collection.find_one({"email": email})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User doesn't exist. Wrong email."
            )

        user = User(**user)

        if not verify_password(password, user.password):
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "You are not authorized. Wrong email or password.",
                headers = {"WWW-Authenticate": "Bearer"}
            )

        access_token = create_access_token(user.id, user.email)
        
        today = datetime.now()
        
        updated_user = self.users_collection.find_one_and_update(
            {"_id": user.id},
            {"$set": {"last_login": str(today)}},
            return_document= ReturnDocument.AFTER
        )
        
        return User(**updated_user), access_token
