# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt


COPY etl ./etl
COPY main_etl.py ./main_etl.py

CMD ["python3","main_etl.py"]