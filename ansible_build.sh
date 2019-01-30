#!/bin/sh

docker build . -t test-runner
docker run --name runner --privileged -v `pwd`:/root/build -d test-runner /sbin/init
docker exec -it runner bash -c "cd /root/build && ansible-playbook site.yml --syntax-check"
docker exec -it runner bash -c "cd /root/build && ansible-playbook site.yml"
docker exec -it runner bash -c "cd /root/build && py.test -v test.py"
docker rm -f runner
