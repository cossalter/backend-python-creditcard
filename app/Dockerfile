FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . .

RUN apt-get update \
    && apt-get install -y \
    g++ \
    gcc \
    gdal-bin \
    git \
    less \
    libavif-dev \
    libjpeg62-turbo \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libproj-dev \
    libwebp-dev \
    locales \
    tar \
    zlib1g \
    && apt-get clean \
    && apt-get autoremove --purge -y

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen
RUN sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen

COPY pyproject.toml .
COPY poetry.lock .
RUN pip install -U pip wheel poetry \
    && poetry export --without-hashes -f requirements.txt -o requirements.txt \
    && pip install -r requirements.txt

EXPOSE 8000
