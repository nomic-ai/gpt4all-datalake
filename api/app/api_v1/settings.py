from pydantic import BaseSettings

class Settings(BaseSettings):
    app_environment = 'dev'
    image_version: str = 'unspecified'
    root_filesystem_path: str = '/home'


settings = Settings()