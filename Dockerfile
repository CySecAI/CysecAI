FROM python:3.11-slim

RUN apt-get update && apt-get install -y python3-dev gcc pipx \
    && rm -rf /var/lib/apt/lists/*

RUN pipx install poetry

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY . .

RUN poetry install

CMD ["poetry", "--version"]
