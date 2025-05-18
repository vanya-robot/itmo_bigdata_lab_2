FROM python:3.9-slim AS builder

WORKDIR /app

COPY setup.py .
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
    
COPY . .
RUN pip install .

FROM python:3.9-slim
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app /app

COPY .env /app/.env

ENV PATH=/usr/local/bin:$PATH
ENV PYTHONPATH=/app

CMD ["sh", "-c", "python -c 'from src.scripts.init_db import init_db; init_db()' && python -m uvicorn src.api.app:app --host 0.0.0.0 --port 8000"]