FROM nginx:1.19.6-alpine

WORKDIR /etc/nginx/ssl
RUN apk add openssl
RUN openssl req -new -text -passout pass:abcd -subj /CN=localhost -out server.req -keyout privkey.pem
RUN openssl rsa -in privkey.pem -passin pass:abcd -out server.key
RUN openssl req -x509 -in server.req -text -days 3650 -key server.key -out server.crt

WORKDIR /code

CMD nginx -g "daemon off;"
