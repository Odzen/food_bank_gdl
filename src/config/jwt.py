from src.config import env_file
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class JWTSettings(BaseSettings):

    jwt_secret_key: str
    jwt_encoding_algorithm: str
    jwt_admin_token: str
    jwt_dev_token: str
    jwt_employee_token: str
    
    model_config = SettingsConfigDict(env_file=env_file, extra='ignore')
    
@lru_cache
def get_settings():
    print("JWT settings: ", JWTSettings())
    return JWTSettings()