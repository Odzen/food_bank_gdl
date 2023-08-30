from src.config import env_file
from pymongo import MongoClient
from pydantic import BaseSettings
import certifi


class DatabaseSettings(BaseSettings):
    db_cluster_domain: str
    db_name: str
    db_username: str
    db_password: str

    class Config:
        env_file = env_file


db_settings = DatabaseSettings()

mongodb_uri = "mongodb+srv://{username}:{password}@{cluster_domain}/?retryWrites=true&w=majority".format(
        username = db_settings.db_username, 
        password = db_settings.db_password, 
        cluster_domain = db_settings.db_cluster_domain)

client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())

db = client[db_settings.db_name]