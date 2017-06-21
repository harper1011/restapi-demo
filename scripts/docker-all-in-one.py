#!/usr/bin/env python
import logging
import subprocess

APP_NAME = 'docker-all-in-one'
FORMAT = '%(asctime)s %(module)s:%(lineno)-3s[%(levelname)s] %(message)s'

logging.basicConfig(filename=APP_NAME+'.txt', format=FORMAT, level=logging.WARN)
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)

REMOVE_REDIS_CONTAINER = 'sudo docker container rm redis -f'
REMOVE_REST_CONTAINER = 'sudo docker container rm restapi-demo -f'

BUILD_REST_DOCKER = "sudo docker build -t restapi-demo ."
RUN_REDIS_DOCKER = "sudo docker run -d --name redis -p 6379:6379 redis"
RUN_REST_DOCKER = "sudo docker run -p 3000:3000 --name restapi-demo -d --link redis:redis restapi-demo"
PS_CMD = "sudo docker ps"
REMOVE_LOGS = "sudo rm -rf *.log"
TEST_CMD = "sudo python SOURCES/test_rest_server.py"

if __name__ == '__main__':
    try:
        r = subprocess.check_output(REMOVE_LOGS, shell=True)
        logger.info("Run '%s' with result:\n%s", REMOVE_LOGS, r)
    except:
        logger.exception('Failed to remove existing logs. Continue....')

    try:
        r = subprocess.check_output(REMOVE_REDIS_CONTAINER, shell=True)
        logger.info("Run '%s' with result:\n%s", REMOVE_REDIS_CONTAINER, r)
    except:
        logger.exception('Failed to remove existing containers. Continue....')

    try:
        r = subprocess.check_output(REMOVE_REST_CONTAINER, shell=True)
        logger.info("Run '%s' with result:\n%s", REMOVE_REST_CONTAINER, r)
    except:
        logger.exception('Failed to remove existing containers. Continue....')

    # TODO: use Docker Compose to do this
    r = subprocess.check_output(BUILD_REST_DOCKER, shell=True)
    logger.info("Run '%s' with result:\n%s", BUILD_REST_DOCKER, r)
    r = subprocess.check_output(RUN_REDIS_DOCKER, shell=True)
    logger.info("Run '%s' with result:\n%s", RUN_REDIS_DOCKER, r)
    r = subprocess.check_output(RUN_REST_DOCKER, shell=True)
    logger.info("Run '%s' with result:\n%s", RUN_REST_DOCKER, r)
    r = subprocess.check_output(PS_CMD, shell=True)
    logger.info("Run '%s' with result:\n%s", PS_CMD, r)
    try:
        r = subprocess.check_output(TEST_CMD, shell=True)
        logger.info("Run '%s' with result:\n%s", TEST_CMD, r)
    except:
        logger.exception('dummy')
    logger.info("Run '%s' with result:\n%s", RUN_REST_DOCKER, r)
    r = subprocess.check_output(PS_CMD, shell=True)