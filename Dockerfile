FROM python

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

WORKDIR /app

RUN poetry install

COPY . /app/

CMD ["/root/.poetry/bin/python3"]

