import click
import os
from jinja2 import Template


_nginx_conf_template = Template("""
worker_processes 1;
 
events { worker_connections 1024; }

http {

    sendfile on;

    server {
        listen 443 ssl;
        client_max_body_size 2G;
        ssl_certificate /certs/public.crt;
        ssl_certificate_key /certs/private.key;

        location / {
            proxy_pass     {{ proxy_pass }};
        proxy_redirect     off;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host $server_name;
        proxy_read_timeout {{ proxy_read_timeout }};
        }
    }
}""")

@click.command()
@click.option("--proxy_pass", help="upstream host url")
@click.option("--proxy_read_timeout", help="nginx timeout")
@click.option("--out", "-o", help="output file")
def create_conf(proxy_pass=None, proxy_read_timeout=None, out=None):
    proxy_pass = proxy_pass or os.getenv("NGINX_UPSTREAM_HOST", "http://mushroom-server:5000")
    proxy_read_timeout = proxy_read_timeout or os.getenv("NGINX_TIMEOUT", 3600)
    conf_str = _nginx_conf_template.render(proxy_pass=proxy_pass, proxy_read_timeout=proxy_read_timeout)

    if not out:
        click.echo(conf_str)
    else:
        with open(out, "w") as f:
            f.write(conf_str)

if __name__ == "__main__":
    create_conf()
