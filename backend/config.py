from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = "your_mongodb_uri_here"  # Replace with your actual URI
    DATABASE_NAME: str = "neothink"

    class Config:
        env_file = ".env"

settings = Settings()
