import pytest
import logging
import os
from pathlib import Path

LOG_DIR = Path("logs/")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def pytest_configure(config):
    """Настройка логирования при запуске тестов"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/testing.log'),
            logging.StreamHandler()
        ]
    )