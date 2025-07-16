from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    BOT_TOKEN: str
    MAIN_ADMIN_ID: int
    LOG_LEVEL: str = Field(default="INFO")

    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "botdb"
    POSTGRES_USER: str = "botuser"
    POSTGRES_PASSWORD: str = "botpass"
    DB_URL: str | None = None

    ADMIN_ERROR_THROTTLE_SEC: int = 60
    BACKUP_DIR: str = "/app/backups"

    @property
    def dsn(self) -> str:
        if self.DB_URL:
            return self.DB_URL
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

settings = Settings()