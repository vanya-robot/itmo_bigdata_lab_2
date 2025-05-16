from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from core.model import PenguinClassifier
from api.schemas import PenguinFeatures
from pathlib import Path
import logging
import time

LOG_DIR = Path("logs/")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "api.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("api logger")

app = FastAPI(title="Penguin Species Classifier API")

# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    logger.info(
        f"Request: {request.method} {request.url} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.2f}ms"
    )
    return response

try:
    model = PenguinClassifier.load('models/penguin_model.pkl')
    
    logger.info("Model loaded successfully")
except Exception as e:
    logger.critical(f"Failed to load model: {str(e)}")
    raise RuntimeError("Cannot start API without model")

@app.post("/predict")
async def predict(features: PenguinFeatures):
    try:
        logger.info(f"Prediction request: {features}")

        prediction = model.predict(features)
        logger.info(f"Prediction result: {prediction[0]}")

        return {"species": prediction[0]}

    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "OK"}