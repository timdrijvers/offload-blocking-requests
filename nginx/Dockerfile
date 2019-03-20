FROM nginx:latest

# Nginx will listen on this port
EXPOSE 80

RUN rm /etc/nginx/conf.d/default.conf

COPY app.conf /etc/nginx/nginx.conf
COPY offloader.js /etc/nginx/offloader.js
