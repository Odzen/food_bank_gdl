from src.config import env_file
from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):

    jwt_secret_key: str
    jwt_encoding_algorithm: str
    jwt_admin_token: str
    jwt_dev_token: str
    jwt_employee_token: str
    model_config = SettingsConfigDict(env_file=env_file, extra="ignore")


jwt_settings = JWTSettings()