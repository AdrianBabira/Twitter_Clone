# Dockerfile

# pull the official docker image
FROM python:latest

RUN apt update && apt install -y postgresql-client

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements_prod.txt .

# install dependencies
RUN pip install -r requirements_prod.txt

# copy project
COPY . .
