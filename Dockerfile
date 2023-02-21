FROM python:3.11

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/
WORKDIR /app

ARG POETRY_ARGS="--no-root --no-dev"
RUN poetry install $POETRY_ARGS

# Copy library
COPY ./app /app
ENV PYTHONPATH="/:${PYTHONPATH}"

CMD ["gunicorn", "app", "--bind", "0.0.0.0:8000"]
