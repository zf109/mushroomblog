#!/bin/sh
# source /entrypoint.sh
python3 ./create_conf.py -o /etc/nginx/nginx.conf
cat /etc/nginx/nginx.conf
nginx -g "daemon off;"
