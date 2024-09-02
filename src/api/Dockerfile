FROM python:3.11-slim
ENV POETRY_VERSION=1.8.1
ENV PORT=8000
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY . .
RUN poetry install --no-root --only=dev

EXPOSE $PORT

CMD ["sh", "-c", "poetry run uvicorn src.asgi:app --log-level trace --host 0.0.0.0 --port $PORT"]
