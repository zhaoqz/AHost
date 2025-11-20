FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project files
COPY . .

# Install dependencies
RUN uv sync --frozen

# Create data directories
RUN mkdir -p data/sites data/db logs

# Expose port
EXPOSE 8000

# Run application
CMD ["uv", "run", "main.py"]
