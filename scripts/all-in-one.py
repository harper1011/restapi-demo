#!/usr/bin/env python
import logging
import subprocess

APP_NAME = 'all_in_one'
FORMAT = '%(asctime)s %(module)s:%(lineno)-3s[%(levelname)s] %(message)s'

logging.basicConfig(filename=APP_NAME+'.log', format=FORMAT, level=logging.WARN)
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)

MAKE_RPM = "sudo make clean rpm"
INSTALL_RPM = "sudo rpm -ivh --replacepkgs simple-restapi-server-*.rpm --force"
ENABLE_SERVICE = "sudo systemctl start restapi"

if __name__ == '__main__':
    r = subprocess.check_output(MAKE_RPM, shell=True)
    logger.info("Run '%s' with result:\n%s", MAKE_RPM, r)

    r = subprocess.check_output(INSTALL_RPM, shell=True)
    logger.info("Run '%s' with result:\n%s", INSTALL_RPM, r)

    r = subprocess.check_output(ENABLE_SERVICE, shell=True)
    logger.info("Run '%s' with result:\n%s", ENABLE_SERVICE, r)
