from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 jours

    # Admin initial — créé en DB au premier démarrage si aucun user n'existe
    admin_username: str
    admin_password_hash: str

    gemini_api_key: str
    upload_dir: str = "/app/uploads"
    max_upload_bytes: int = 10 * 1024 * 1024  # 10 Mo

    # SMTP (optionnel — si absent, les mails ne sont pas envoyés)
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = ""
    app_base_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()
