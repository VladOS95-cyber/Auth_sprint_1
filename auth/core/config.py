import os
from datetime import timedelta
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

SWAGGER_CONFIG = {
    "headers": [
    ],
    "openapi": "3.0.2",
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/openapi/",
    "url_prefix": "/api",
}

PROJECT_NAME = os.getenv('PROJECT_NAME', 'auth')

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6389))

POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5433))
POSTGRES_NAME = os.getenv('POSTGRES_NAME', 'auth_database')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'auth')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 1234)
POSTGRES_OPTIONS = os.getenv('POSTGRES_OPTIONS', '-c search_path=users')

FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
BASE_URL = os.getenv('BASE_URL', '/api/v1')


JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 1)))
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2)))
JWT_ERROR_MESSAGE_KEY = os.getenv('JWT_ERROR_MESSAGE_KEY', 'message')


class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str = Field(JWT_SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = Field(JWT_ACCESS_TOKEN_EXPIRES)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = Field(JWT_REFRESH_TOKEN_EXPIRES)
    JWT_ERROR_MESSAGE_KEY: str = Field(JWT_ERROR_MESSAGE_KEY)


class PostgresSettings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = Field(
        f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
        f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}', description='url for auth service'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True


class RedisSettings(BaseSettings):
    REDIS_URI: str = Field(f'redis://{REDIS_HOST}:{REDIS_PORT}')
