FROM python:3.8.16-slim
ENV PIPENV_PIPFILE=/app/Pipfile

RUN apt update
RUN apt install -y git vim

RUN mkdir /app
COPY ./*.py ./LICENSE ./Pip* ./README.md /app/
RUN cd /app

RUN pip install pipenv
RUN pipenv install

WORKDIR /app

ENV PWD=/app
#CMD ["java", "-Djava.security.egd=file:/dev/./urandom", "-jar", "/app/java-spring-vuly-0.1.0.jar"]
