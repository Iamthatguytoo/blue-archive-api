from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str
    CLIENT: str
    DATABASE: str

    API_COLLECTION: str = "blue_archive_students"
    API_COLLECTION_KEYS: str = "blue_archive_api_secret_keys"

    API_COLLECTION_SCRAPER: str

    class Config:
        env_file = ".env.local"


settings = Settings()