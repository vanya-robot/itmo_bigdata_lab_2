import logging
import zipfile
import os
from pathlib import Path
from core.model import PenguinClassifier
from core.config import load_config_to_dict
from core.exceptions import ModelSaveError, ModelTrainingError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def ensure_data_ready(zip_path: str = 'penguin_dataset.zip') -> str:
    csv_path = 'data/raw/penguins_size.csv'

    if os.path.exists(csv_path):
        logger.info(f"Data already exists at {csv_path}")
        return csv_path

    if os.path.exists(zip_path):
        logger.info(f"Extracting {zip_path}...")
        try:
            os.makedirs('data/raw', exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extract('penguins_size.csv', 'data/raw')
            logger.info(f"Successfully extracted to {csv_path}")
            return csv_path
        except Exception as e:
            logger.error(f"Extraction failed: {str(e)}")
            raise

    logger.error("No data found! Please provide either:")
    logger.error(f"1. {zip_path} in project root")
    logger.error(f"2. {csv_path} in prepared state")
    raise FileNotFoundError("Training data not available")

def main():
    try:
        logger.info("Starting training process...")
        
        data_path = ensure_data_ready()
        config = load_config_to_dict('configs/config.ini')

        model = PenguinClassifier(config)
        accuracy = model.train(data_path)
        try:
            model.save('models/penguin_model.pkl')
            logger.info(f"Training completed successfully! Accuracy: {accuracy:.2f}")
        except ModelSaveError as e:
            logger.critical(f"Saving failed: {str(e)}")
        
    except ModelTrainingError as e:
        logger.critical(f"Training pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()