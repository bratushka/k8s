FROM python:3.9.1-alpine3.13

WORKDIR /code

RUN apk add --no-cache \
    gcc \
    libffi-dev \
    make \
    musl-dev \
    linux-headers \
    openrc \
    openssh \
    python3-dev \
    postgresql-dev

COPY ./requirements.txt .
RUN pip install --upgrade pip wheel setuptools
RUN pip install -r requirements.txt

CMD ./manage.py runserver 0.0.0.0:8000
