FROM python:3.11-slim as base

ENV PIPENV_PIPFILE=/app/Pipfile
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/app

RUN apt update && \
    apt install -y git vim && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /app

COPY ./*.py ./LICENSE ./Pip* ./README.md /app/
RUN cd /app && \
    pip install pipenv && \
    pipenv install --system && \
    git config --global --add safe.directory /repo

WORKDIR /repo

FROM base as contributors-github
ENTRYPOINT ["/app/github-repo-committers.py"]

FROM base as contributors-local
ENTRYPOINT ["/app/local-repo-committers.py"]
