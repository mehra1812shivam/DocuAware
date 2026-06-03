from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    environment: str

    database_url: str = ""

    jwt_secret: str = ""

    qdrant_url: str = ""
    qdrant_api_key: str = ""

    grok_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()