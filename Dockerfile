FROM python:3.7-alpine
# FROM nginx:1.16-alpine
# FROM ubuntu:latest

# RUN adduser -D pc_donation
# RUN useradd -M pc_donation

WORKDIR /home/pc_donation

COPY requirements.txt requirements.txt
# COPY requirements_new.txt requirements_new.txt
RUN apk add --no-cache --update gcc musl-dev libffi-dev openssl-dev nginx supervisor

# RUN apk install python3-pip python3-setuptools python3-venv
# RUN apk add --no-cache --update gcc musl-dev libffi-dev openssl-dev python3-dev python3 supervisor
# RUN apk add --no-cache --virtual .build-deps g++ python3-dev gcc musl-dev libffi-dev openssl-dev && \
#     pip3 install --upgrade pip setuptools && \
#     pip3 install -r requirements.txt && \
#     apk del .build-deps
# RUN apk add --no-cache --update python3

RUN python3 -m venv venv
# RUN python3.7 -m venv venv
RUN venv/bin/pip3 install --upgrade pip
RUN venv/bin/pip3 install -r requirements.txt
# RUN venv/bin/pip3 install -r requirements_new.txt
RUN venv/bin/pip3 install azure-ai-formrecognizer --pre
RUN venv/bin/pip3 install gunicorn
# RUN venv/bin/pip3 uninstall JWT -y
# RUN venv/bin/pip3 uninstall PyJWT -y
# RUN venv/bin/pip3 install PyJWT


COPY app app
COPY migrations migrations
COPY pc_donation.py config.py webconfig.py run.py boot.sh nginx.sh web.sh ./
RUN chmod +x boot.sh nginx.sh web.sh

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/default.conf
COPY project.conf /etc/nginx/conf.d/
RUN mkdir -p /run/nginx

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV FLASK_APP run.py

# RUN chown -R pc_donation:pc_donation ./
# RUN chown -R pc_donation:pc_donation /etc/nginx/
# RUN chown -R pc_donation:pc_donation /etc/nginx/nginx.conf
# RUN chown -R pc_donation:pc_donation /etc/nginx/conf.d/project.conf
# RUN chown -R pc_donation:pc_donation /var/lib/nginx/
# USER pc_donation

EXPOSE 80 443 5000
ENTRYPOINT ["./web.sh"]
