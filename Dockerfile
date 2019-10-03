 # Pull base image
 FROM python:3.7-slim

 # Set environment varibles
 ENV PYTHONDONTWRITEBYTECODE 1
 ENV PYTHONUNBUFFERED 1

 # Set work directory
 WORKDIR /code

 # Install dependencies
 COPY Pipfile Pipfile.lock /code/
 RUN pip install pipenv && pipenv install --system

 # create user
 RUN useradd -ms /bin/bash newuser
 USER newuser

 # Copy project
 COPY . /code/