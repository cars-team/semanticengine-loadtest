FROM python:3.7

CMD mkdir -p /usr/src/myapp/
COPY locustfile.py /usr/src/myapp/
WORKDIR /usr/src/myapp/

RUN pip install locustio

#CMD locust --no-web -c 1000 -r 100

CMD locust --master --master-bind-port=5557 2> locust-master-stderr.txt 1> locust-master-stdout.txt

#CMD ["tail", "-f", "/dev/null"]
