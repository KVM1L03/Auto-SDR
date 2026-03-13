from dotenv import load_dotenv

load_dotenv()

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: SecretStr
    tavily_api_key: SecretStr
    langchain_api_key: SecretStr | None = None
    langchain_tracing_v2: bool = False
    langchain_project: str = "auto-sdr"
    cors_origins: str = "http://localhost:5173"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()