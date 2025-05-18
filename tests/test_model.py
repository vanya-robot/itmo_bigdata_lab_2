import pytest
import logging
from src.model import PenguinClassifier
from src.exceptions import ModelTrainingError
from src.data_processing import DataProcessor

logger = logging.getLogger("model test logger")

@pytest.fixture
def model():
    return PenguinClassifier.load('experiments/penguin_model.pkl')

@pytest.fixture
def processor():
    return DataProcessor()

def test_model_prediction(model):
    from src.api.schemas import PenguinFeatures 

    """Тестирование предсказаний модели"""
    test_sample = {'island': 'Torgersen',
        'culmen_length_mm': 39.1,
        'culmen_depth_mm': 18.7,
        'flipper_length_mm': 181.0,
        'body_mass_g': 3750.0,
        'sex': 'MALE'
        }
    
    try:
        logger.info("Starting model prediction test")
        logger.debug(f"Test sample: {test_sample}")

        logger.debug("Transforming dict to pydantic")
        validated = PenguinFeatures.model_validate(test_sample)

        logger.debug("Calling model.predict()")

        prediction = model.predict(validated)
        
        logger.info(f"Model prediction: {prediction}")
        assert prediction in ['Adelie', 'Gentoo', 'Chinstrap'], "Invalid prediction"
        
        logger.info("Model prediction test completed successfully")
        
    except Exception as e:
        logger.error(f"Model prediction failed: {str(e)}")
        logger.exception("Exception details:")
        pytest.fail(f"Model prediction failed: {str(e)}")