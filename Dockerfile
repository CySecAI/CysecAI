FROM python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN curl -sSL https://install.python-poetry.org | python3 -

# ENV PATH="/root/.poetry/bin:$PATH"
COPY pyproject.toml poetry.lock /app/

WORKDIR /app

RUN poetry install

COPY . /app/


CMD ["/root/.poetry/bin/python3"]
