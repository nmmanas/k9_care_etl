# Use an official Python runtime as a parent image
FROM python:3.9-slim

# copy and install requirements
COPY requirements.txt /tmp/requirements.txt

# Set the working directory in the container
WORKDIR /usr/src/app

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# copy the pipeline files
COPY etl ./etl

# copy the test cases
COPY tests ./tests
# copy __init__.py file for tests 
COPY __init__.py ./__init__.py

# copy main etl script file
COPY main_etl.py ./main_etl.py

# command to run the script
CMD ["python3","main_etl.py"]