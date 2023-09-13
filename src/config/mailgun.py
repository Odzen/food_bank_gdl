from src.config import env_file
from pydantic_settings import BaseSettings, SettingsConfigDict


class MailgunSettings(BaseSettings):

    mailgun_api_url: str
    mailgun_domain: str
    mailgun_api_key: str
    mailgun_from: str
    model_config = SettingsConfigDict(env_file=env_file, extra="ignore")

mailgun_settings = MailgunSettings()