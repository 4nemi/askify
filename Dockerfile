FROM python:3.10.12-slim as builder

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10.12-slim

WORKDIR /code

COPY --from=builder /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./askify /code/askify

CMD [ "uvicorn", "askify.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080" ]