import pytest
from core.data_processing import DataProcessor
from core.exceptions import DataProcessingError

def test_data_processing():
    processor = DataProcessor()
    try:
        X_train, X_test, y_train, y_test = processor.process('data/raw/penguins_size.csv')
        assert X_train.shape[0] > 0
        assert X_test.shape[0] > 0
    except Exception as e:
        pytest.fail(f"Data processing failed: {str(e)}")