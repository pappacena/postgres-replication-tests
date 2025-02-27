FROM python:3.10-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv venv && uv run ls

COPY . /app/

CMD uv run python hello.py