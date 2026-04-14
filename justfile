# refinery — development commands

install:
    uv sync --all-groups

lint:
    uv run pre-commit run --all-files

test:
    uv run pytest tests/ -v --cov=src --cov-report=term-missing

coverage:
    uv run coverage run -m pytest tests/ -v --cov=src --cov-report=html

version-check:
    uv run cz bump --dry-run --yes || [ $? -eq 21 ]
