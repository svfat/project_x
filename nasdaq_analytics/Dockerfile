FROM python:3.6-alpine
ENV BUILD_REQUIREMENTS "gcc musl-dev libxml2-dev libxslt-dev libffi-dev"
ENV REQUIREMENTS "libxml2 libxslt postgresql-dev"

RUN mkdir -p /srv/nasdaq_analitics
WORKDIR /srv/nasdaq_analitics

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN apk update --no-cache \
    && apk add --no-cache $BUILD_REQUIREMENTS $REQUIREMENTS \
    && pip install -r requirements.txt \
    && apk del $BUILD_REQUIREMENTS

COPY . .
RUN chmod +x scraper.py