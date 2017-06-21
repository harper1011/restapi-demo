FROM ubuntu
MAINTAINER Dapeng Jiao <harper1011@gmail.com>

WORKDIR /opt/script/restapi/

COPY SOURCES/*.py /opt/script/restapi/
COPY SOURCES/requirements.txt /opt/script/restapi/
RUN apt-get update && apt-get -y upgrade && apt-get install -y python-dev python-pip curl
RUN pip install --upgrade pip && pip install -r /opt/script/restapi/requirements.txt

EXPOSE 3000

HEALTHCHECK --interval=10s --timeout=2s CMD curl -f http://localhost:3000/api/v1/ || exit 1
ENTRYPOINT python /opt/script/restapi/simple_rest_server.py '0.0.0.0' 3000