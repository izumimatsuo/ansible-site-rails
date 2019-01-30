FROM williamyeh/ansible:centos7

RUN yum -y update && yum -y install docker && yum -y install git
RUN pip install --upgrade pip setuptools && pip install testinfra

WORKDIR /root
CMD ["/bin/bash"]
