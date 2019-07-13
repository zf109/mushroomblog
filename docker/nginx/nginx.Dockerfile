FROM nginx:alpine
# COPY nginx.conf /etc/nginx/nginx.conf
# COPY bin/s3fs /usr/bin/s3fs
RUN mkdir certs
COPY nginx/certs/selfsigned.crt /certs/public.crt
COPY nginx/certs/selfsigned.key /certs/private.key
COPY nginx/setup.sh /setup.sh
# COPY base/entrypoint.sh /entrypoint.sh
RUN chmod +x /setup.sh && /setup.sh

COPY nginx/create_conf.py /create_conf.py
COPY nginx/entrypoint-nginx.sh /entrypoint-nginx.sh
RUN chmod +x /entrypoint-nginx.sh 
ENTRYPOINT /entrypoint-nginx.sh
