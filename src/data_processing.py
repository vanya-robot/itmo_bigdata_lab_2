import pandas as pd
import logging
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from src.exceptions import DataValidationError, FeatureProcessingError
from configparser import ConfigParser
from typing import Dict, Any
from pathlib import Path

LOG_DIR = Path("logs/")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/processing.log'),
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
                ('cat', OneHotEncoder(handle_unknown='ignore'), ['island', 'sex'])
            ],
            remainder='passthrough'  # Числовые признаки остаются без изменений
        )
    
    
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
        try:
            df = pd.read_csv(data_path)
            if df.empty:
                raise DataValidationError("Empty dataset")
                
            df = df.dropna()
            if df.empty:
                raise DataValidationError("No valid data after NA removal")
                
            X = df.drop('species', axis=1)
            y = df['species']
            
            X_processed = self.preprocessor.fit_transform(X)
            return train_test_split(X_processed, y, 
                                  test_size=self.config['test_size'],
                                  random_state=self.config['random_state'])
        except pd.errors.EmptyDataError as e:
            raise DataValidationError("CSV file is empty or corrupt")
        
        except KeyError as e:
            raise DataValidationError(f"Missing required column: {str(e)}")
        
        except Exception as e:
            raise FeatureProcessingError(f"Data processing failed: {str(e)}")

    def transform_single(self, features: dict) -> np.array:
        try:
            df = pd.DataFrame([features])
            processed = self.preprocessor.transform(df)
            return processed
        
        except ValueError as e:
            raise FeatureProcessingError(f"Invalid feature values: {str(e)}")
        
        except AttributeError as e:
            raise FeatureProcessingError("Preprocessor not fitted yet")
        
        except Exception as e:
            raise FeatureProcessingError(f"Feature transformation failed: {str(e)}")

    def fit(self, df: pd.DataFrame):
        """Обучение препроцессора на данных"""
        self.preprocessor.fit(df)
        # Получаем имена фичей после преобразования
        self.feature_names = self.preprocessor.get_feature_names_out()
        return self

    def get_feature_names(self):
        """Возвращает имена фичей после преобразования"""
        if self.feature_names is None:
            raise RuntimeError("Processor not fitted yet")
        return self.feature_names