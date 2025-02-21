FROM python:3.12-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk add --no-cache \
    curl


RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN mkdir /src
COPY pyproject.toml poetry.lock /src/
WORKDIR /src/
RUN poetry install -vv --no-root

COPY / /src/