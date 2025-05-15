import pytest
import logging
from core.model import PenguinClassifier
from core.exceptions import ModelTrainingError

logger = logging.getLogger(__name__)

@pytest.fixture
def model():
    return PenguinClassifier('configs/config.ini')

def test_model_training(model):
    """Тестирование обучения модели с логированием"""
    test_data_path = 'data/raw/penguins.csv'
    
    try:
        logger.info(f"Starting model training test with data: {test_data_path}")
        
        logger.debug("Calling model.train()")
        accuracy = model.train(test_data_path)
        
        logger.info(f"Model trained with accuracy: {accuracy:.2f}")
        assert 0 <= accuracy <= 1, "Invalid accuracy value"
        
        logger.info("Model training test completed successfully")
        
    except Exception as e:
        logger.error(f"Model training failed: {str(e)}")
        logger.exception("Exception details:")
        pytest.fail(f"Model training failed: {str(e)}")

def test_model_prediction(model):
    """Тестирование предсказаний модели с логированием"""
    test_sample = {
        'island': 'Torgersen',
        'culmen_length_mm': 39.1,
        'culmen_depth_mm': 18.7,
        'flipper_length_mm': 181.0,
        'body_mass_g': 3750.0,
        'sex': 'MALE'
    }
    
    try:
        logger.info("Starting model prediction test")
        logger.debug(f"Test sample: {test_sample}")
        
        # Обучаем модель сначала
        model.train('data/raw/penguins.csv')
        
        logger.debug("Calling model.predict()")
        prediction = model.predict(test_sample)
        
        logger.info(f"Model prediction: {prediction}")
        assert prediction in ['Adelie', 'Gentoo', 'Chinstrap'], "Invalid prediction"
        
        logger.info("Model prediction test completed successfully")
        
    except Exception as e:
        logger.error(f"Model prediction failed: {str(e)}")
        logger.exception("Exception details:")
        pytest.fail(f"Model prediction failed: {str(e)}")