# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    MPLCONFIGDIR=/tmp/matplotlib

WORKDIR /app

# Runtime libs for common scientific Python wheels (scikit-learn/matplotlib)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libgomp1 \
        libfreetype6 \
        libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

# Install uv (https://github.com/astral-sh/uv)
RUN pip install --no-cache-dir uv

# Copy dependency metadata first for better layer caching
COPY pyproject.toml uv.lock ./

# Create venv + install locked runtime dependencies (without installing this project)
RUN uv sync --frozen --no-dev --no-install-project

# Copy the application code
COPY README.md ./
COPY ml_framework_project ./ml_framework_project

# Install this project so console scripts (entry points) are available
RUN uv pip install --no-deps .

EXPOSE 8000

CMD ["uvicorn", "ml_framework_project.api:app", "--host", "0.0.0.0", "--port", "8000"]
