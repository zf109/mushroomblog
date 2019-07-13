#!/bin/sh
apk update && apk add python3
python3 -m ensurepip
pip3 install --upgrade pip
pip3 install click==6.7 jinja2==2.8.1
