from src.config import env_file
from pymongo import MongoClient
import certifi
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib import parse
from pydantic import ValidationError
from typing import Optional

class DatabaseSettings(BaseSettings):
    db_cluster_domain: str
    db_name: str
    db_username: Optional[str] = None
    db_password: Optional[str] = None
    db_local: bool
    model_config = SettingsConfigDict(env_file=env_file, extra='ignore')

db_settings = None
try:
    db_settings = DatabaseSettings()
except ValidationError as e:
    print(e)

if db_settings.db_local:
    mongodb_local_uri = f"mongodb://{db_settings.db_cluster_domain}/{db_settings.db_name}"

    client = MongoClient(mongodb_local_uri)
    
else:
    mongodb_uri = "mongodb+srv://{username}:{password}@{cluster_domain}/?retryWrites=true&w=majority".format(
            username=parse.quote_plus(db_settings.db_username),
            password=parse.quote_plus(db_settings.db_password),
            cluster_domain = db_settings.db_cluster_domain
    )
    
    client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())

db = client[db_settings.db_name]