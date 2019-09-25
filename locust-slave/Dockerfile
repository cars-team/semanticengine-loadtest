FROM python:3.7

CMD mkdir -p /usr/src/myapp/
COPY locustfile.py /usr/src/myapp/
WORKDIR /usr/src/myapp/

RUN pip install locustio

#CMD locust --no-web -c 1000 -r 100
CMD locust --slave --master-host=engine-cont --master-port=5557

