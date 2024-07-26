from src.config.jwt import get_settings as jwt_settings
from jose import jwt
import bcrypt


def create_access_token(user_id: str, email: str):
    data_to_encode = {"id": str(user_id), "email": email}
    
    encoded_jwt = jwt.encode(data_to_encode, jwt_settings().jwt_secret_key, jwt_settings().jwt_encoding_algorithm)

    return encoded_jwt

def _hash_password(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password

# Check if the provided password matches the stored password (hashed)
def _verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
        
    return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password)
    
def get_hashed_password(password):
    return _hash_password(password)

def verify_password(plain_password, stored_hashed_password) -> bool:
    return _verify_password(plain_password, stored_hashed_password)