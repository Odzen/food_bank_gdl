from bson import ObjectId
from src.config.auth import oauth2_scheme, optional_oauth2_scheme
from src.config.jwt import get_settings as jwt_settings
from src.models.users import User, Roles
from src.services.users import UserService
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from src.models import PyObjectId


SECRET_KEY = jwt_settings().jwt_secret_key
JWT_ALGORITHM = jwt_settings().jwt_encoding_algorithm


def get_user_from_access_token(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    user_id = None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [JWT_ALGORITHM])
        user_id = payload.get("id")
    except JWTError:
        raise credentials_exception

    if user_id is None:
        raise credentials_exception

    user = UserService().get_user_by_ID(user_id)

    if user is None:
        raise credentials_exception

    return user


def get_optional_user_from_access_token(token: str = Depends(optional_oauth2_scheme)) -> User|None:
    if not token:
        return None
    
    return get_user_from_access_token(token)

def user_is_dev(user: User = Depends(get_user_from_access_token)):
    if user.role != Roles.developer:
        raise HTTPException(
            detail = "You need to be developer to perform this action.",
            status_code = status.HTTP_401_UNAUTHORIZED
        )

    return user

def user_is_admin(user: User = Depends(get_user_from_access_token)):
    if user.role != Roles.admin:
        raise HTTPException(
            detail = "You need to be admin to perform this action.",
            status_code = status.HTTP_401_UNAUTHORIZED
        )

    return user

def user_is_admin_or_dev(user: User = Depends(get_user_from_access_token)):
    if user.role != Roles.admin and user.role != Roles.developer:
        raise HTTPException(
            detail = "You need to be admin or dev to perform this action.",
            status_code = status.HTTP_401_UNAUTHORIZED
        )

    return user

def user_is_owner(
    user_id: PyObjectId, # Id of the user owner of the resource to be accesed
    user_from_token: User = Depends(get_user_from_access_token)
):
    user_id = ObjectId(user_id)

    if user_id != user_from_token.id:
        raise HTTPException(
            detail = "You need to be the owner of the resource you are trying to access.",
            status_code = status.HTTP_401_UNAUTHORIZED
        )

    return user_from_token


def user_is_owner_or_employee(
    user_id: PyObjectId, # Id of the user owner of the resource to be accesed
    user_from_token: User = Depends(get_user_from_access_token)
):
    user_id = ObjectId(user_id)

    if (not user_from_token.role == Roles.employee) and user_id != user_from_token.id:
        raise HTTPException(
            detail = "You need to be the either owner of the resource you are trying to access or a system employee.",
            status_code = status.HTTP_401_UNAUTHORIZED
        )

    return user_from_token

def user_is_owner_or_admin(
    user_id: PyObjectId, # Id of the user owner of the resource to be accesed
    user_from_token: User = Depends(get_user_from_access_token)
):
    user_id = ObjectId(user_id)

    if (not user_from_token.role == Roles.admin) and user_id != user_from_token.id:
        raise HTTPException(
            detail = "You need to be the either owner of the resource you are trying to access or a system admin.",
            status_code = status.HTTP_401_UNAUTHORIZED
        )

    return user_from_token

def user_is_owner_or_dev(
    user_id: PyObjectId, # Id of the user owner of the resource to be accesed
    user_from_token: User = Depends(get_user_from_access_token)
):
    user_id = ObjectId(user_id)

    if (not user_from_token.role == Roles.developer) and user_id != user_from_token.id:
        raise HTTPException(
            detail = "You need to be the either owner of the resource you are trying to access or a system dev.",
            status_code = status.HTTP_401_UNAUTHORIZED
        )

    return user_from_token

def user_roles_checks(user_action: User, user: User = Depends(get_user_from_access_token)) -> None:
    if user.role == Roles.developer:
        return
    
    if user.role == Roles.employee:
        raise HTTPException(
            detail = "Employees can't create users.",
            status_code = status.HTTP_401_UNAUTHORIZED
        )
    
    if user.role == Roles.admin and user_action.role == Roles.developer:
        raise HTTPException(
            detail = "Unauthorized Role. Admins can manage only admins or employees.",
            status_code = status.HTTP_401_UNAUTHORIZED
        )
        
    return