FROM python:3.6-alpine
ENV BUILD_REQUIREMENTS "git gcc musl-dev libxml2-dev libxslt-dev libffi-dev"
ENV REQUIREMENTS "bash make libxml2 libxslt postgresql-dev postgresql-client"

RUN mkdir -p /srv/project_x
WORKDIR /srv/project_x

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN apk update --no-cache \
    && apk add --no-cache $BUILD_REQUIREMENTS $REQUIREMENTS \
    && pip install -r requirements.txt \
    && apk del $BUILD_REQUIREMENTS

COPY . .
RUN chmod +x nasdaq_analytics/scraper.sh
RUN chmod +x migrations/apply.sh
