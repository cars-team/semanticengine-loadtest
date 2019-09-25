FROM openjdk:9
CMD mkdir -p /usr/src/myapp/
COPY semanticengine-1.0.1-SNAPSHOT-jar-with-dependencies.jar /usr/src/myapp/
COPY lsa_experiments_tb.ttl /usr/src/myapp/
WORKDIR /usr/src/myapp/

CMD ["java","-jar","semanticengine-1.0.1-SNAPSHOT-jar-with-dependencies.jar","-tb","lsa_experiments_tb.ttl"]
#CMD ["tail", "-f", "/dev/null"]
