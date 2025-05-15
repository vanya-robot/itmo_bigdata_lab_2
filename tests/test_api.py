import pytest
from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

@pytest.mark.parametrize("test_input,expected", [
    ({
        "island": "Torgersen",
        "culmen_length_mm": 39.1,
        "culmen_depth_mm": 18.7,
        "flipper_length_mm": 181.0,
        "body_mass_g": 3750.0,
        "sex": "MALE"
    }, 200),
    ({
        "island": "Unknown",
        "culmen_length_mm": -1,  # Invalid value
        "culmen_depth_mm": 18.7,
        "flipper_length_mm": 181.0,
        "body_mass_g": 3750.0,
        "sex": "MALE"
    }, 422)
])
def test_predict_endpoint(test_input, expected):
    response = client.post("/predict", json=test_input)
    assert response.status_code == expected