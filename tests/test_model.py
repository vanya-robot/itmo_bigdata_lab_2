import pytest
from core.model import PenguinClassifier
from core.exceptions import ModelTrainingError

def test_model_training():
    model = PenguinClassifier('configs/config.ini')
    accuracy = model.train('data/raw/penguins.csv')
    assert 0 <= accuracy <= 1
    
def test_model_prediction():
    model = PenguinClassifier('configs/config.ini')
    model.train('data/raw/penguins.csv')
    sample = {
        'island': 'Torgersen',
        'culmen_length_mm': 39.1,
        'culmen_depth_mm': 18.7,
        'flipper_length_mm': 181.0,
        'body_mass_g': 3750.0,
        'sex': 'MALE'
    }
    prediction = model.predict(sample)
    assert prediction in ['Adelie', 'Gentoo', 'Chinstrap']