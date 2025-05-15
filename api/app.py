from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.model import PenguinClassifier
import joblib
from .schemas import PenguinFeatures

app = FastAPI()
model = PenguinClassifier.load('models/penguin_model.pkl')

@app.post("/predict")
async def predict(features: PenguinFeatures):
    try:
        processed = model.data_processor.transform_single(features.dict())
        prediction = model.predict(processed)
        return {"species": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))