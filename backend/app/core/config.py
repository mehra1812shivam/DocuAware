from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    environment: str

    database_url: str = ""

    jwt_secret: str = ""
    jwt_algorithm: str = ""
    access_token_expire_minutes: int = 30

    qdrant_url: str = ""
    qdrant_api_key: str = ""
    qdrant_collection: str = ""

    grok_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()