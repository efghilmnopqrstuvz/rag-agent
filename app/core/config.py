from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Legge automaticamente le variabili da .env
    # Il nome dell'attributo deve corrispondere alla variabile in .env
    openai_api_key: str
    model_name: str = "gpt-4"  # valore di default se non specificato in .env
    app_env: str = "development"

    class Config:
        env_file = ".env"  # dice a Pydantic dove trovare il file

# Istanza singleton — viene creata una volta sola e importata ovunque
settings = Settings()