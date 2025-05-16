from setuptools import setup, find_packages
from pathlib import Path

LOG_DIR = Path("logs/")
LOG_DIR.mkdir(parents=True, exist_ok=True)

setup(
    name="penguin_classifier",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'scikit-learn>=1.0',
        'pandas>=1.3',
        'fastapi>=0.68',
        'uvicorn>=0.15',
        'pydantic>=1.8',
        'joblib>=1.0',
        'python-dotenv>=0.19',
        'httpx>=0.28.1'
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'requests>=2.26'
        ]
    },
    python_requires='>=3.9',
    include_package_data=True 
)