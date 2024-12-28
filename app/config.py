from typing import List

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    weaviate_host: str = "http://localhost"
    # weaviate_port: str = "8080"
    weaviate_key: str = ""
    weaviate_batch: int = 100
    huggingface_key: str = ""
    hf_embeddings_batch: int = 1600
    num_of_threads: int = 4
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    env: str = "local"
    admin_secret: str = "admin-secret-key"
    allowed_origins: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class CorsSettings(BaseSettings):
    allow_origins: str = "*"
    allow_credentials: bool = True
    allow_methods: str = "*"
    allow_headers: str = "*"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class JwtSettings(BaseSettings):
    secret_key: str = ""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class DatabaseSettings(BaseSettings):
    db_host: str = "localhost"
    db_user: str = "user"
    db_port: int = 3306
    db_database: str = "db"
    db_password: str = "password"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
cors_settings = CorsSettings()
jwt_settings = JwtSettings()
database = DatabaseSettings()
