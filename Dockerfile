FROM python:3.10

ENV ENV_TYPE=production \
  TZ=Europe/Helsinki \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.1

RUN apt-get update && \
    apt-get install -y libpq-dev gcc tk

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi --no-root

COPY . /app

ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_HOST=$POSTGRES_HOST
ENV TELEGRAM_TOKEN=$TELEGRAM_TOKEN
ENV OPENAI_KEY=$OPENAI_KEY

CMD ["poetry", "run", "python", "main.py"]
