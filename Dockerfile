FROM ghcr.io/astral-sh/uv:debian-slim AS builder

ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_PREFERENCE=only-managed

RUN uv python install 3.12

WORKDIR /app
ADD patcher.py pyproject.toml uv.lock /app
RUN uv sync --frozen --no-dev --no-editable

FROM gcr.io/distroless/cc

WORKDIR /app
COPY --from=builder --chown=python:python /python /python
COPY --from=builder --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "/app/patcher.py"]