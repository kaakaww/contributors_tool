FROM python:3.8.16-slim as base

ENV PIPENV_PIPFILE=/app/Pipfile
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/app

RUN apt update
RUN apt install -y git vim

RUN mkdir /app
COPY ./*.py ./LICENSE ./Pipfile ./README.md /app/
RUN cd /app

RUN pip install pipenv
RUN pipenv install --system

WORKDIR /repo

FROM base as contributors-github
ENTRYPOINT /app/github-repo-committers.py

FROM base as contributors-local
ENTRYPOINT /app/local-repo-committers.py
