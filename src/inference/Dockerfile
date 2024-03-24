# Use the official Python image as the base image
FROM python:3.12-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /code

# Install poetry
RUN pip install "poetry"

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Creating layers for project files:
COPY . /code


# Start vunicorn
CMD ["uvicorn", "main:app", "--port", "9001"]
