import pytest
import logging
from core.data_processing import DataProcessor
from core.exceptions import DataProcessingError

logger = logging.getLogger(__name__)

@pytest.fixture
def processor():
    return DataProcessor()

def test_data_processing(processor):
    test_file = 'data/raw/penguins_size.csv'
    
    try:
        logger.info(f"Starting data processing test with file: {test_file}")
        
        logger.debug("Calling processor.process()")
        X_train, X_test, y_train, y_test = processor.process(test_file)
        
        logger.info(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")
        assert X_train.shape[0] > 0, "Empty training data"
        assert X_test.shape[0] > 0, "Empty test data"
        
        logger.info("Data processing test completed successfully")
        
    except Exception as e:
        logger.error(f"Data processing failed: {str(e)}")
        logger.exception("Exception details:")
        pytest.fail(f"Data processing failed: {str(e)}")