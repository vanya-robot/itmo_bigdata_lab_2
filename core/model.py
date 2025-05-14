import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class PenguinModel:
    """Класс для работы с моделью классификации пингвинов"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        
        self._island_map = {'Torgersen': 0, 'Biscoe': 1, 'Dream': 2}
        self._sex_map = {'MALE': 0, 'FEMALE': 1}
        self._species_map = {'Adelie': 0, 'Gentoo': 1, 'Chinstrap': 2}
        self._inv_species_map = {v: k for k, v in self._species_map.items()}

    def preprocess(self, data: pd.DataFrame) -> tuple:
        """Подготовка данных"""
        df = data.dropna().copy()
        df['island'] = df['island'].map(self._island_map)
        df['sex'] = df['sex'].map(self._sex_map)
        y = df['species'].map(self._species_map)
        
        features = ['island', 'culmen_length_mm', 'culmen_depth_mm', 
                   'flipper_length_mm', 'body_mass_g', 'sex']
        X = df[features]
        
        return X, y

    def train(self, data_path: str):
        """Обучение модели"""
        df = pd.read_csv(data_path)
        X, y = self.preprocess(df)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict(self, features: dict) -> str:
        """Предсказание вида пингвина"""
        df = pd.DataFrame([features])
        df['island'] = df['island'].map(self._island_map)
        df['sex'] = df['sex'].map(self._sex_map)
        
        X = self.scaler.transform(df)
        pred = self.model.predict(X)[0]
        return self._inv_species_map[pred]

    def save(self, path: str):
        """Сохранение модели"""
        joblib.dump({'model': self.model, 'scaler': self.scaler}, path)

    @classmethod
    def load(cls, path: str) -> 'PenguinModel':
        """Загрузка модели"""
        instance = cls()
        data = joblib.load(path)
        instance.model = data['model']
        instance.scaler = data['scaler']
        return instance