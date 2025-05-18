import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from src.data_processing import DataProcessor
from src.exceptions import ModelTrainingError, ModelSaveError
from typing import Dict, Any
from pathlib import Path
from src.api.schemas import PenguinFeatures

class PenguinClassifier:
    def __init__(self, config: Dict[str, Any] = None, **kwargs):
        self.config = {
            'n_estimators': 100,
            'max_depth': None,
            **({} if config is None else config),
            **kwargs
        }
        
        self.model = RandomForestClassifier(
            n_estimators=self.config['n_estimators'],
            max_depth=self.config['max_depth']
        )
        
        self.data_processor = DataProcessor(config)
        self.is_trained = False

    def train(self, data_path):
        try:
            X_train, X_test, y_train, y_test = self.data_processor.process(data_path)
            self.model.fit(X_train, y_train)
            
            y_pred = self.model.predict(X_test)
            self.accuracy = accuracy_score(y_test, y_pred)
            self.is_trained = True
            
            return self.accuracy
        except Exception as e:
            raise ModelTrainingError(f"Training failed: {str(e)}")

    def predict(self, features: PenguinFeatures):
        if not self.is_trained:
            raise ValueError("Model is not trained yet")
        
        features_dict = features.dict()

        processed = self.data_processor.transform_single(features_dict)
        return self.model.predict(processed)

    def save(self, path):
        """Сохраняет модель, создавая директорию при необходимости"""
        try:
            # Создаем директорию, если ее нет
            model_path = Path(path)
            model_path.parent.mkdir(parents=True, exist_ok=True)
            
            joblib.dump({
                'model': self.model,
                'accuracy': self.accuracy,
                'data_processor': self.data_processor,
                'config': self.config  # Сохраняем конфиг для восстановления
            }, path)
            
        except Exception as e:
            raise ModelSaveError(f"Failed to save model: {str(e)}")

    @classmethod
    def load(cls, path):
        loaded = joblib.load(path)
        instance = cls()
        instance.model = loaded['model']
        instance.accuracy = loaded['accuracy']
        instance.data_processor = loaded['data_processor']
        instance.is_trained = True
        instance.config = loaded['config']
        return instance