import pandas as pd
import logging
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from configparser import ConfigParser
from typing import Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)

class DataProcessor:
    def __init__(self, config: Dict[str, Any] = None, **kwargs):
        config = ConfigParser()
        full_config = {**(config or {}), **kwargs}

        defaults = {
            'test_size': 0.2,
            'random_state': 123456,
        }
        
        # Применяем конфиг с проверкой типов
        self.config = {**defaults, **self._validate_config(full_config)}
        
        logging.info(f"DataProcessor config: {self.config}")

        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), ['culmen_length_mm', 'culmen_depth_mm', 
                 'flipper_length_mm', 'body_mass_g']),
                ('cat', OneHotEncoder(), ['island', 'sex'])
            ])
    
    
    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Валидация и преобразование типов"""
        validated = {}
        
        if 'test_size' in config:
            try:
                validated['test_size'] = float(config['test_size'])
            except (ValueError, TypeError) as e:
                logging.warning(f"Invalid test_size, using default. Error: {e}")
        
        if 'random_state' in config:
            try:
                validated['random_state'] = int(config['random_state'])
            except (ValueError, TypeError) as e:
                logging.warning(f"Invalid random_state, using default. Error: {e}")
        
        return validated

    def process(self, data_path):
        df = pd.read_csv(data_path)
        df = df.dropna()
        
        X = df.drop('species', axis=1)
        y = df['species']
        
        X_processed = self.preprocessor.fit_transform(X)
        return train_test_split(X_processed, y, 
                              test_size=self.config['test_size'],
                              random_state=self.config['random_state'])