FROM python:3.7.5-stretch
WORKDIR /app/src
COPY . .
RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake
RUN  pip install -r requirements.txt
CMD python api.py
