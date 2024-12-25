FROM python:3.10-slim-buster as builder

WORKDIR /app

# Install uv
RUN pip install uv

# Copy pyproject.toml and lock file (if available)
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

# Install dependencies with uv (using lock file for reproducibility)
RUN uv pip install .


FROM python:3.10-slim-buster

WORKDIR /app

COPY --from=builder /app /app

# Expose the port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]