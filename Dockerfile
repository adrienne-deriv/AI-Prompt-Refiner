FROM python:3.9-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uvicorn", "project.server:app", "--reload", "--port", "8000", "--host", "0.0.0.0"]