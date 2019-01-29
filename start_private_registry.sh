#!/bin/sh

docker ps |grep registry || docker run -d -p 5000:5000 --name registry registry:2.3.0
docker build . -t localhost:5000/ansible/test-runner
docker push localhost:5000/ansible/test-runner
