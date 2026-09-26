from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):

  APP_NAME: str
  APP_VERSION: str

  PDF_PATH: str
  JSON_PATH: str


  class Config:
    env_file = ".env"

def get_settings() -> Settings:
  return Settings()
