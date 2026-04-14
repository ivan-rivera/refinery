FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.6.0 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev
COPY src/ ./src/
EXPOSE 8000
CMD ["uv", "run", "gunicorn", "src.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
