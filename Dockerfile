
FROM python:3.12-slim

WORKDIR /code

RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/
