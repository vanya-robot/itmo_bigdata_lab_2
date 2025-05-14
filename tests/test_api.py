from fastapi.testclient import TestClient
from api.app import app
import json

client = TestClient(app)

def test_predict_endpoint():
    test_data = {
        "island": "Torgersen",
        "culmen_length_mm": 39.1,
        "culmen_depth_mm": 18.7,
        "flipper_length_mm": 181.0,
        "body_mass_g": 3750.0,
        "sex": "MALE"
    }
    response = client.post("/predict", json=test_data)
    assert response.status_code == 200
    assert "species" in response.json()