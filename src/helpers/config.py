from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):




  class Config:
    env_file = ".env"

def get_settings() -> Settings:
  return Settings()
