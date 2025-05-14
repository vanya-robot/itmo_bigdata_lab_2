class ModelTrainingError(Exception):
    """Ошибка при обучении модели"""
    pass

class DataProcessingError(Exception):
    """Ошибка обработки данных"""
    pass

class PredictionError(Exception):
    """Ошибка при предсказании"""
    pass