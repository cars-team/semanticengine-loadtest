FROM python:3.7

CMD mkdir -p /usr/src/myapp/
COPY locustfile.py /usr/src/myapp/
COPY .env /usr/src/myapp/
WORKDIR /usr/src/myapp/

RUN pip install locustio
RUN pip install locust-plugins
#RUN pip install -e git://github.com/locustio/locust.git@master#egg=locustio

#CMD locust --no-web -c 1000 -r 100

CMD locust --master --port 8089 --master-bind-port 5557 2> locust-master-stderr.txt 1> locust-master-stdout.txt

#CMD ["tail", "-f", "/dev/null"]
