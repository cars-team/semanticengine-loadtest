#!/bin/bash

cp files/lsa_experiments_ab.ttl files/lsa_experiments_tb.ttl files/semanticengine-1.0.1-SNAPSHOT-jar-with-dependencies.jar docker-engine/engine/
cp files/locustfile.py docker-locust/locust-master/
cp files/locustfile.py docker-locust/locust-slave/

cp .env docker-engine/.env
cp .env docker-locust/.env

cp .env docker-engine/engine/.env
cp .env docker-locust/locust-master/.env
cp .env docker-locust/locust-slave/.env

#cd docker-engine/
#docker-compose stop
#docker-compose rm -f
#docker-compose build
#docker-compose --compatibility up -d
#cd ..

cd docker-locust/
docker-compose stop
docker-compose rm -f
docker-compose build
docker-compose --compatibility up -d
cd ..
