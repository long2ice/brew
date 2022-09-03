from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    DB_URL: str
    REDIS_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
TORTOISE_ORM = {
    "apps": {
        "models": {
            "models": ["brew.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "connections": {"default": settings.DB_URL},
}
