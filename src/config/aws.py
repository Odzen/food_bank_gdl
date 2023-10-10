import boto3
from src.config import env_file
from pydantic_settings import BaseSettings, SettingsConfigDict


class AWSSettings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
        
    model_config = SettingsConfigDict(env_file=env_file, extra='ignore')




aws_settings = AWSSettings()

s3_client = boto3.client(
    "s3",
    aws_access_key_id = aws_settings.aws_access_key_id,
    aws_secret_access_key = aws_settings.aws_secret_access_key
)


images_bucket_name = "food-bank-bucket"