from pydantic import BaseModel, Field, validator
from typing import Literal

class PenguinFeatures(BaseModel):
    island: Literal['Torgersen', 'Biscoe', 'Dream'] = Field(
        ..., 
        example="Torgersen",
        description="Island name must be one of: Torgersen, Biscoe, Dream"
    )
    
    culmen_length_mm: float = Field(
        ..., 
        example=39.1,
        gt=0,
        le=100,
        description="Culmen length in mm (0 < value <= 100)"
    )
    
    culmen_depth_mm: float = Field(
        ..., 
        example=18.7,
        gt=0,
        le=30,
        description="Culmen depth in mm (0 < value <= 30)"
    )
    
    flipper_length_mm: float = Field(
        ..., 
        example=181.0,
        gt=0,
        le=250,
        description="Flipper length in mm (0 < value <= 250)"
    )
    
    body_mass_g: float = Field(
        ..., 
        example=3750.0,
        gt=0,
        le=10000,
        description="Body mass in grams (0 < value <= 10000)"
    )
    
    sex: Literal['MALE', 'FEMALE'] = Field(
        ..., 
        example="MALE",
        description="Sex must be either MALE or FEMALE"
    )

    @validator('*', pre=True)
    def replace_empty_with_none(cls, v):
        return None if v == "" else v

class PredictionResponse(BaseModel):
    species: Literal['Adelie', 'Gentoo', 'Chinstrap'] = Field(
        ..., 
        example="Adelie"
    )
