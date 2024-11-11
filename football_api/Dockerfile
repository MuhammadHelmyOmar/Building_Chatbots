# pull Python official base image
FROM python:3.9.19-bullseye

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# set some environment variables (these prevents python from generating some extra files)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get install -y curl software-properties-common libpq-dev build-essential libssl-dev

# install python dependencies
RUN pip install --upgrade pip

# Copy requirements.txt for caching the pip install step and install other dependencies
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt --default-timeout=1000000

# copy all files in src
COPY ./src .

# run the app
ENTRYPOINT [ "uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0", "--workers", "1"]