from pydantic import BaseModel, Field

class PenguinFeatures(BaseModel):
    island: str = Field(..., example="Torgersen")
    culmen_length_mm: float = Field(..., example=39.1)
    culmen_depth_mm: float = Field(..., example=18.7)
    flipper_length_mm: float = Field(..., example=181.0)
    body_mass_g: float = Field(..., example=3750.0)
    sex: str = Field(..., example="MALE")

class PredictionResponse(BaseModel):
    species: str = Field(..., example="Adelie")
    probability: float = Field(..., example=0.95)