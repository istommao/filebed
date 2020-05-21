FROM centos/python-36-centos7

USER root

RUN mkdir -p /var/www/

ADD requirements.txt /tmp/requirements.txt
ADD src /var/www/src
ADD static /var/www/static
ADD main.py /var/www

RUN echo -e "\
[mongodb]\n\
name=MongoDB Repository\n\
baseurl=https://repo.mongodb.org/yum/redhat/7Server/mongodb-org/4.2/x86_64/\n\
gpgcheck=0\n\
enabled=1\n" >> /etc/yum.repos.d/mongodb.repo

RUN yum update -y && yum install -y mongodb-org &&\
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

# Set up directory requirements
RUN mkdir -p ./mongodb /var/log/mongodb /var/run/mongodb
VOLUME ["./mongodb", "/var/log/mongodb"]

# Expose port 27017 from the container to the host
EXPOSE 27017
