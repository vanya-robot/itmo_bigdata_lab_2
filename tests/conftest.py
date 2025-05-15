import pytest
import logging
import os

def pytest_configure(config):
    """Настройка логирования при запуске тестов"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('tests/test_logs.log'),
            logging.StreamHandler()
        ]
    )