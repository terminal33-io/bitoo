FROM python:3.11-bullseye

# Install system dependencies including cmake - needed for sentencepiece package
RUN apt-get update && apt-get install -y cmake build-essential

# Set the working directory inside the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files first to leverage Docker layer caching
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install poetry

# Export Poetry dependencies to a requirements.txt file
RUN poetry export --without-hashes -f requirements.txt -o requirements.txt

# Install the dependencies via pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Expose the port FastAPI will use
EXPOSE 9090

# Command to run FastAPI using Uvicorn
CMD ["uvicorn", "app.chat:app", "--host", "0.0.0.0", "--port", "9090"]