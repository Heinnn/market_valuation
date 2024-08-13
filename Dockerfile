FROM python:3.9
MAINTAINER hi@jitta

RUN apt-get update
RUN pip install pipenv --upgrade

WORKDIR /code

ADD Pipfile Pipfile.lock /code
RUN pipenv install --deploy

# COPY .env /code
ADD . /code

WORKDIR /code
CMD pipenv run python loop_peband_monthly.py
