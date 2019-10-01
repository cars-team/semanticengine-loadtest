FROM python:3.7

CMD mkdir -p /usr/src/myapp/
COPY locustfile.py /usr/src/myapp/
COPY .env /usr/src/myapp/
WORKDIR /usr/src/myapp/

RUN pip install -e git://github.com/locustio/locust.git@master#egg=locustio
#RUN pip install locustio

#CMD locust --no-web -c 1000 -r 100

CMD locust --slave --master-host=locust-master --master-port=5557 2> locust-slave-stderr.txt 1> locust-slave-stdout.txt

#CMD ["tail", "-f", "/dev/null"]
