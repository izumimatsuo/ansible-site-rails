#!/bin/sh

docker ps | grep test-runner || (docker build . -t test-runner && docker run --name test-runner --privileged -v `pwd`:/root/build -p 8080:80 -d test-runner /sbin/init)
docker exec -it test-runner bash -lc "cd /root/build && ansible-galaxy install -r requirements.yml"
docker exec -it test-runner bash -lc "cd /root/build && ansible-playbook site.yml --syntax-check"
docker exec -it test-runner bash -lc "cd /root/build && ansible-playbook site.yml"
docker exec -it test-runner bash -lc "cd /root/build && py.test -v tests"
#docker rm -f test-runner
