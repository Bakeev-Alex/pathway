FROM python:3.12-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk add --no-cache \
    curl


RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN mkdir /app
COPY pyproject.toml poetry.lock /app/
WORKDIR /app/
RUN poetry install -vv --no-root

COPY / /app/

CMD ["python", "src/telegram_bot/main_tg.py"]