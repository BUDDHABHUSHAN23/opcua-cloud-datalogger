FROM python:3.11-slim-bookworm

WORKDIR /app

# Copy everything from the current context into /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
