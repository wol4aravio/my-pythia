FROM python:3.8.6-slim

RUN apt-get update && apt-get install -y git

RUN pip3 install poetry

WORKDIR /src
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-dev

COPY mypythia mypythia
RUN poetry install --no-dev

ENTRYPOINT [ "poetry", "run" ]
