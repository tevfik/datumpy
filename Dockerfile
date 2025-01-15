FROM python:3.10-slim

WORKDIR /app

COPY datum.py requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "datum:app", "--host", "0.0.0.0", "--port", "8000"]
