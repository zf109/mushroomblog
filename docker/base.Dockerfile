FROM python:3.7-stretch

RUN apt-get update && apt-get install -y vim libfreetype6 libfreetype6-dev libpng-dev libxft-dev
RUN apt-get update && apt-get install -y freetds-dev freetds-bin unixodbc-dev libgnutls-openssl27 libffi-dev sox ffmpeg postgresql
RUN apt-get update && apt-get install -y python3-pip
RUN apt-get update && apt-get install -y autotools-dev automake libtool sox libsox-fmt-mp3 texinfo git praat gcc

RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get update && apt-get install -y tdsodbc python3-pyodbc
RUN apt-get update && apt-get install -y libfuse-dev libcurl4-gnutls-dev gnutls-dev

COPY ./requirements/requirements.txt /requirements.txt

RUN pip3 install -U setuptools
RUN pip3 install --upgrade pip

RUN pip3 install -r /requirements.txt
RUN pip3 install -U "celery[redis]"
