from pydantic_settings import BaseSettings
from urllib.parse import quote

class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_MINUTES: int

    @property
    def DATABASE_URL(self):
        quoted_password = quote(self.DATABASE_PASSWORD, safe="")
        return (
            f"postgresql://{self.DATABASE_USERNAME}:{quoted_password}@"
            f"{self.DATABASE_HOSTNAME}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True
