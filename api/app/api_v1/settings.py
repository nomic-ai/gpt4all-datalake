from pydantic import BaseSettings

class Settings(BaseSettings):
    app_environment = 'dev'
    image_version: str = 'unspecified'
    root_filesystem_path: str = '/home'
    gpt4all_datalake_bucket: str = ''


settings = Settings()