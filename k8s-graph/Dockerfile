FROM neo4j:4.2.3

WORKDIR $NEO4J_HOME/certificates/bolt
RUN openssl req -new -text -passout pass:abcd -subj /CN=localhost -out server.req -keyout privkey.pem
RUN openssl rsa -in privkey.pem -passin pass:abcd -out server.key
RUN openssl req -x509 -in server.req -text -days 3650 -key server.key -out server.crt
RUN chmod og-rwx server.key

WORKDIR $NEO4J_HOME/conf
COPY .conf ./.conf
RUN cat .conf >> neo4j.conf

WORKDIR $NEO4J_HOME

CMD ["neo4j"]
