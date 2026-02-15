from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./dev.db"
    JWT_SECRET: str = "dev-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 10080
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    REDIS_URL: str = "redis://localhost:6379/0"
    MAX_FILE_SIZE: int = 10485760
    UPLOAD_DIR: str = "./uploads"
    GENERATED_DIR: str = "C:/Downloads/generated_projects"
    
    class Config:
        env_file = ".env"

settings = Settings()
