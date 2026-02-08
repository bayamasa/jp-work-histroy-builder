FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src/ src/
COPY fonts/ fonts/
COPY sample/ sample/

ENTRYPOINT ["uv", "run", "python", "-m", "jb_workhistory"]
