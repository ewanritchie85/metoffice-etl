# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Default command (adjust this to your actual entrypoint)
CMD ["python", "src/main/main.py"]