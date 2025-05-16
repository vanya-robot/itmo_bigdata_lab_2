API Start:

from python venv:
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000

without entering venv:
python -m uvicorn api.app:app --reload --host 0.0.0.0 --port 8000

API Request:

curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{
  "island": "Torgersen",
  "culmen_length_mm": 39.1,
  "culmen_depth_mm": 18.7,
  "flipper_length_mm": 181.0,
  "body_mass_g": 3750.0,
  "sex": "MALE"
}'