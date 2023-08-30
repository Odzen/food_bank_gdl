from src.config import env_file
from pydantic import BaseSettings


class JWTSettings(BaseSettings):

    jwt_secret_key: str
    jwt_encoding_algorithm: str

    class Config:
        env_file = env_file


jwt_settings = JWTSettings()