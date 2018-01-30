FROM centos:7
MAINTAINER LCO Webmaster <webmaster@lco.global>

EXPOSE 80
ENTRYPOINT [ "/init" ]

# Setup the Python Django environment
ENV PYTHONPATH /var/www/whatsup
ENV DJANGO_SETTINGS_MODULE whatsupapp.settings

# Set the PREFIX env variable
ENV PREFIX /whatsup

# install and update packages
RUN yum -y install epel-release \
        && yum -y install MySQL-python python-pip nginx supervisor uwsgi-plugin-python \
        && yum -y update \
        && yum -y clean all

# install python requirements
COPY requirements.txt /var/www/whatsup/requirements.txt
RUN pip install --upgrade pip \
        && pip install -r /var/www/whatsup/requirements.txt \
        && rm -rf /root/.cache /root/.pip

# install configuration
COPY docker/ /

# install webapp
COPY . /var/www/whatsup
