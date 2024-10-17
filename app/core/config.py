from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings, extra="allow"):
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")
    DEBUG: bool = Field(True, env="DEBUG")

    OLLAMA_API_URL: str = Field(..., env="OLLAMA_API_URL")
    OLLAMA_MODEL_NAME: str = Field(..., env="OLLAMA_MODEL_NAME")

    CELERY_BROKER_URL: str = Field(..., env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(..., env="CELERY_RESULT_BACKEND")

    class Config:
        env_file = ".env"


settings = Settings()
