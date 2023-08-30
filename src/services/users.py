from src.models import PyObjectId
from src.config.db import db
from src.models.users import User
from src.schemas.users import (
    UserRetrieved, UpdateUser, CreateUser, Roles)
from bson import ObjectId
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from src.utils.cryptography import get_hashed_password
from typing import List

class UserService():

    def __init__(self):
        self.users_collection = db["users"]
        
    def get_user_by_ID(self, id: PyObjectId) -> User:
        
        user = self.users_collection.find_one({"_id": ObjectId(id)})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User doesn't exist. Wrong ID."
            )

        return User(**user)
    
    def get_user_by_email(self, email: EmailStr) -> User:
        user = self.users_collection.find_one({"email": {"$regex": f"^{email}$", "$options": "i"}})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User doesn't exist. Wrong email."
            )

        return UserRetrieved(**user)
    
    def list_all_users(self, role: Roles = None) -> List[UserRetrieved]:
        users = []
        
        aggregate_query = []
        base_query = {}
        aggregate_query.append({"$match": base_query})
        
        if role:
            base_query["role"] = role
            
        # user_requesting = self.get_user_by_ID(user_id)
        
        # if user_requesting.role == Roles.admin:
        #     aggregate_query.append({"$match": {"role": {"$ne": Roles.developer}}})

        users_found = self.users_collection.aggregate(aggregate_query)
        
        for user_document in users_found:
            user = UserRetrieved(**user_document)
            users.append(user)

        return users
    
    def update_user_by_ID(self, id: PyObjectId, user: UpdateUser) -> UpdateUser:
        user_dict = jsonable_encoder(user, exclude_none = True)

        try:
            updated_user = self.users_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": user_dict},
                return_document=ReturnDocument.AFTER
            )

            if not updated_user:
                raise HTTPException(
                    detail=f"User with the id={id} doesn't exist",
                    status_code=status.HTTP_409_CONFLICT
                )
        except DuplicateKeyError as e:
            raise HTTPException(
                detail="User with that email already exists: " + e.details["errmsg"],
                status_code=status.HTTP_409_CONFLICT
            )

        return UserRetrieved(**updated_user)
    
    
    def create(self, user_to_create: CreateUser, user_id_creator: PyObjectId | None = None) -> User:
        
        user_to_create = jsonable_encoder(user_to_create)
        user_to_create["email"] = user_to_create["email"].lower()
        user_to_create["password"] = get_hashed_password(user_to_create["password"])
        
        user_to_create = User(**user_to_create)

        user_to_save = jsonable_encoder(user_to_create)
        del user_to_save["_id"]
        
        try:
            inserted_user = self.users_collection.insert_one(user_to_save)
            
            self.users_collection.find_one_and_update(
                {"_id": inserted_user.inserted_id},
                {"$set": {"created_by": user_id_creator}},
                return_document= ReturnDocument.AFTER
            )
            
        except DuplicateKeyError as e:
            error_message = e.details.get("errmsg")
            print(error_message)
            if "email" in error_message:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
            elif "id" in error_message:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Id already exists")
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Duplicate key error")

        user_id = inserted_user.inserted_id
        
        user = UserService().get_user_by_ID(user_id)

        return user
