# Dockerfile
FROM python:3.9-slim

# Install Poetry
RUN pip install poetry

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . /app

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Command to run the script (will be overridden by Docker Compose if needed)
CMD ["python", "init_db.py"]
