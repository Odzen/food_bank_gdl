from src.config.jwt import jwt_settings
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = jwt_settings.jwt_secret_key
JWT_ALGORITHM = jwt_settings.jwt_encoding_algorithm

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")


def create_access_token(user_id: str, email: str):
    data_to_encode = {"id": str(user_id), "email": email}

    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, JWT_ALGORITHM)

    return encoded_jwt

def get_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, stored_hashed_password) -> bool:
    return pwd_context.verify(plain_password, stored_hashed_password)