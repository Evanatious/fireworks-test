FROM python:3.12.3 AS base

WORKDIR /opt/app
COPY . .
RUN pip3 install -r ./requirements.txt
CMD python3 /opt/app/main.py
