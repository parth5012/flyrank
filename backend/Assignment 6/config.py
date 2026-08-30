from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    LLM_BASE_URL: str
    LLM_API_KEY: str
    LLM_MODEL: str
    LLM_STUB: bool
    LLM_ENABLED: bool = True
    
    DATABASE_URL: str

    SUPABASE_KEY: str
    SUPABASE_URL: str
    PORT: int

    DB_PASS: str

    class Config:
        env_file = ".env"
