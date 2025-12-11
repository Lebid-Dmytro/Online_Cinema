FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.7.1

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Configure poetry and install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy application code
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 8000

# Use entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

