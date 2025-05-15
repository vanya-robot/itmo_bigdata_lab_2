FROM python:3.9-slim

WORKDIR /app

COPY setup.py .
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -e . && \
    pip install -r requirements.txt


COPY . .

ENV PYTHONPATH=/app

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]