from configparser import ConfigParser
from pathlib import Path
from typing import Dict, Any
from pydantic import BaseSettings

def load_config(config_path: str = 'config.ini') -> ConfigParser:
    config = ConfigParser()
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    config.read(config_path)
    return config

def save_config(config: ConfigParser, config_path: str = 'config.ini'):
    with open(config_path, 'w') as f:
        config.write(f)

def load_config_to_dict(config_path: str) -> Dict[str, Any]:
    """Загружает .ini файл и возвращает как словарь"""
    config = ConfigParser()
    config.read(config_path)
    
    result = {}
    for section in config.sections():
        result[section.lower()] = dict(config[section])
    
    return result

class Settings(BaseSettings):
    database_url: str = "postgresql://test_user:test_pass@localhost:5432/test_db"  # Дефолт для CI/CD
    postgres_port: int = 5432
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"  # Игнорировать лишние переменные

settings = Settings()