# OPC Cloud Datalogger
{
  "id": 1,
  "name": "X1",
  "endpoint_url": "opc.tcp://192.168.5.189:62640/IntegrationObjects/ServerSimulator"
}


# BACKUP YAML FILE 
version: "3.9"

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    volumes:
      - ./backend/templates:/app/templates  
    environment:
      - PYTHONPATH=/app/backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis
      - influxdb

  celery:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.celery_app.celery worker --loglevel=info
    depends_on:
      - backend
      - redis
      - db
      - influxdb
    env_file:
      - .env

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: opclogger
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis
    ports:
      - "6379:6379"

  influxdb:
    image: influxdb:2.7
    container_name: opc-cloud-datalogger-influxdb
    ports:
      - "8086:8086"
    volumes:
      - influxdb-data:/var/lib/influxdb2
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_PASSWORD=admin123
      - DOCKER_INFLUXDB_INIT_ORG=opclogger
      - DOCKER_INFLUXDB_INIT_BUCKET=mainbucket
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-secret-token

  frontend:
    build:
      context: ./opc-cloud-frontend
    ports:
      - "5173:5173"
    command: npm run dev -- --host
    working_dir: /app
    depends_on:
      - backend


  test:
    build:
      context: ./backend
      dockerfile: Dockerfile
    working_dir: /app                  # ✅ IMPORTANT: not /app/backend
    command: pytest tests/ --cov=app --cov-report=term --cov-report=xml
    depends_on:
      - db
      - redis
      - influxdb
    env_file:
      - .env
    environment:
      - PYTHONPATH=/app



volumes:
  pgdata:
  influxdb-data:
