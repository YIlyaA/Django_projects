FROM docker.io/nginx:1.27.4-alpine3.21-slim

RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx.conf /etc/nginx/conf.d/default.conf