FROM centos/python-36-centos7

USER root

RUN mkdir -p /var/www/

ADD requirements.txt /tmp/requirements.txt
ADD src /var/www/src
ADD static /var/www/static
ADD main.py /var/www

RUN pip install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com && \
    pip install --no-cache-dir -r /tmp/requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
