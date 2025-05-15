from configparser import ConfigParser
from pathlib import Path
from typing import Dict, Any

def load_config(config_path: str = 'configs/config.ini') -> ConfigParser:
    config = ConfigParser()
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    config.read(config_path)
    return config

def save_config(config: ConfigParser, config_path: str = 'configs/config.ini'):
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