FROM redis:6.2.0-alpine

RUN apk add openssl

RUN mkdir /ssl
WORKDIR /ssl
RUN openssl req -new -text -passout pass:abcd -subj /CN=localhost -out server.req -keyout privkey.pem
RUN openssl rsa -in privkey.pem -passin pass:abcd -out server.key
RUN openssl req -x509 -in server.req -text -days 3650 -key server.key -out server.crt

CMD redis-server \
  --port 0 \
  --tls-port 6379 \
  --tls-cert-file /ssl/server.crt \
  --tls-key-file /ssl/server.key \
  --tls-auth-clients no \
  --requirepass $REDIS_PASSWORD
