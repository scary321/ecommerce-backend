from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_HOSTNAME:str
    DATABASE_PORT:int
    DATABASE_NAME:str
    DATABASE_USERNAME:str
    DATABASE_PASSWORD:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    RAZORPAY_KEY_ID:str
    RAZORPAY_KEY_SECRET:str
    RAZORPAY_WEBHOOK_SECRET:str
    
    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()