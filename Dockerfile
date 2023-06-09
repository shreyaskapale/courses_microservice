FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python3 tests.py

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "app:app"]