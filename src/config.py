from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
  )

  database_url: str = "postgresql+asyncpg://ita:ita_secret@localhost:5432/ita_db"

  @property
  def database_url_sync(self) -> str:
    """URL síncrona para Alembic (usa psycopg2 em vez de asyncpg)."""
    return self.database_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")


settings = Settings()
