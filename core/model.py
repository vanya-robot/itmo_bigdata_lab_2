import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from .data_processing import DataProcessor
from .exceptions import ModelTrainingError

class PenguinClassifier:
    def __init__(self, config_path='configs/config.ini'):
        self.model = RandomForestClassifier()
        self.data_processor = DataProcessor(config_path)
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

    def predict(self, features):
        if not self.is_trained:
            raise ValueError("Model is not trained yet")
        return self.model.predict(features)

    def save(self, path):
        joblib.dump({
            'model': self.model,
            'accuracy': self.accuracy,
            'data_processor': self.data_processor
        }, path)

    @classmethod
    def load(cls, path):
        loaded = joblib.load(path)
        instance = cls()
        instance.model = loaded['model']
        instance.accuracy = loaded['accuracy']
        instance.data_processor = loaded['data_processor']
        instance.is_trained = True
        return instance