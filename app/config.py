import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    _database_url = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root:senha@localhost:3306/estoque_db"
    )
    if _database_url.startswith("postgres://"):
        _database_url = _database_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _database_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key")