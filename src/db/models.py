from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    island = Column(String)
    culmen_length_mm = Column(Float)
    culmen_depth_mm = Column(Float)
    flipper_length_mm = Column(Float)
    body_mass_g = Column(Float)
    sex = Column(String)
    predicted_species = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())