from src.config import env_file
from pymongo import MongoClient
import certifi
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib import parse
from typing import Optional
from functools import lru_cache


class DatabaseSettings(BaseSettings):
    db_cluster_domain: str
    db_name: str
    db_username: Optional[str] = None
    db_password: Optional[str] = None
    db_local: str
    model_config = SettingsConfigDict(env_file=env_file, extra='ignore')

@lru_cache
def get_settings():
    return DatabaseSettings()

if bool(get_settings().db_local):
    mongodb_local_uri = f"mongodb://{get_settings().db_cluster_domain}/{get_settings().db_name}"

    client = MongoClient(mongodb_local_uri)
    
else:
    mongodb_uri = "mongodb+srv://{username}:{password}@{cluster_domain}/?retryWrites=true&w=majority".format(
            username=parse.quote_plus(get_settings().db_username),
            password=parse.quote_plus(get_settings().db_password),
            cluster_domain = get_settings().db_cluster_domain
    )
    
    client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())

db = client[get_settings().db_name]