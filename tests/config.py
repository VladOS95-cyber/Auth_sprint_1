import os
from datetime import timedelta

from pydantic import BaseSettings, Field

REDIS_HOST_TEST = os.getenv('REDIS_HOST_TEST', '127.0.0.1')
REDIS_PORT_TEST = int(os.getenv('REDIS_PORT_TEST', 6389))

POSTGRES_HOST_TEST = os.getenv('POSTGRES_HOST_TEST', '127.0.0.1')
POSTGRES_PORT_TEST = int(os.getenv('POSTGRES_PORT_TEST', 5433))
POSTGRES_NAME_TEST = os.getenv('POSTGRES_NAME_TEST', 'auth_database_test')
POSTGRES_USER_TEST = os.getenv('POSTGRES_USER_TEST', 'postgres')
POSTGRES_PASSWORD_TEST = os.getenv('POSTGRES_PASSWORD_TEST', 1234)
POSTGRES_OPTIONS_TEST = os.getenv('POSTGRES_OPTIONS_TEST', '-c search_path=users')

FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
BASE_URL = os.getenv('BASE_URL', '/api/v1')

JWT_SECRET_KEY_TEST = os.getenv('JWT_SECRET_KEY_TEST', 'super-secret')
JWT_ACCESS_TOKEN_EXPIRES_TEST = timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_TEST', 5)))
JWT_REFRESH_TOKEN_EXPIRES_TEST = timedelta(minutes=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES_TEST', 20)))
JWT_ERROR_MESSAGE_KEY_TEST = os.getenv('JWT_ERROR_MESSAGE_KEY_TEST', 'message')


class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str = Field(JWT_SECRET_KEY_TEST)
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = Field(JWT_ACCESS_TOKEN_EXPIRES_TEST)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = Field(JWT_REFRESH_TOKEN_EXPIRES_TEST)
    JWT_ERROR_MESSAGE_KEY: str = Field(JWT_ERROR_MESSAGE_KEY_TEST)


class PostgresSettings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = Field(
        f'postgresql+psycopg2://{POSTGRES_USER_TEST}:{POSTGRES_PASSWORD_TEST}'
        f'@{POSTGRES_HOST_TEST}:{POSTGRES_PORT_TEST}/{POSTGRES_NAME_TEST}', description='url for auth service'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True


class RedisSettings(BaseSettings):
    REDIS_URI: str = Field(f'redis://{REDIS_HOST_TEST}:{REDIS_PORT_TEST}')
