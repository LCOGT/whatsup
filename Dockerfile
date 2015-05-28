FROM centos:centos7
MAINTAINER Ira W. Snyder <isnyder@lcogt.net>

# nginx on port 80
EXPOSE 80
ENTRYPOINT [ "/init" ]

# Setup the Python Django environment
ENV PYTHONPATH /var/www/whatsup
ENV DJANGO_SETTINGS_MODULE whatsupapp.settings

# install and update packages
RUN yum -y install epel-release \
        && yum -y install gcc make mysql-devel python-devel python-pip sqlite-devel \
        && yum -y install nginx supervisor \
        && yum -y update \
        && yum -y clean all

# install configuration
COPY docker/processes.ini /etc/supervisord.d/
COPY docker/nginx/* /etc/nginx/
COPY docker/uwsgi.ini /etc/
COPY docker/init /init

# install webapp
COPY . /var/www/whatsup

# install Python packages
RUN pip install -r /var/www/whatsup/pip-requirements.txt

# static files
RUN python /var/www/whatsup/manage.py collectstatic --noinput
