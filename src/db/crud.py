from sqlalchemy.orm import Session
from src.db import models
from src.api.schemas import PenguinFeatures

def save_prediction(db: Session, features: PenguinFeatures, prediction: str):
    db_prediction = models.Prediction(
        island=features.island,
        culmen_length_mm=features.culmen_length_mm,
        culmen_depth_mm=features.culmen_depth_mm,
        flipper_length_mm=features.flipper_length_mm,
        body_mass_g=features.body_mass_g,
        sex=features.sex,
        predicted_species=prediction
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction