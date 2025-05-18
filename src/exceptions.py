class ModelTrainingError(Exception):
    """Ошибка при обучении модели"""
    pass

class DataProcessingError(Exception):
    """Ошибка обработки данных"""
    pass

class ModelSaveError(Exception):
    """Ошибка при сохранении модели"""
    pass

class ModelLoadError(Exception):
    """Ошибка при загрузке модели"""
    pass

class PredictionError(Exception):
    """Ошибка во время предсказания"""
    pass

class DataValidationError(Exception):
    """Ошибка валидации данных"""
    pass

class FeatureProcessingError(Exception):
    """Ошибка обработки признаков"""
    pass

class DataExtractionError(Exception):
    """Ошибка извлечения данных"""
    pass

class DataNotFoundError(Exception):
    """Данные не найдены"""
    pass