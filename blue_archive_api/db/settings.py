from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CLIENT: str
    DATABASE: str

    API_COLLECTION: str = "THE_API_COLLECTION"
    API_COLLECTION_KEYS: str = "THE_API_KEY_COLLECTION"

    class Config:
        pass 

settings = Settings()
