#!/usr/bin/env python
import json
import logging
import os
import sys
from collections import OrderedDict

import bottle
import redis

APP_NAME = 'simple_rest_server'
FORMAT = '%(asctime)s %(module)s:%(lineno)-3s[%(levelname)s] %(message)s'
ROOT_URL_PATH = '/api/v1/'
TEST_URL_PATH = '/tst/v1/'

logging.basicConfig(format=FORMAT, level=logging.WARN)
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)

REDIS_IP = os.getenv('REDIS_PORT_6379_TCP_ADDR', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT_6379_TCP_PORT', 6379)
redis_client = redis.StrictRedis(host=REDIS_IP, port=REDIS_PORT, db=0)
try:
    redis_client.info()
    logger.info('Connect to RedisDB successfully. Use RedisDB for storing data.')
    _fake_db = None
except Exception as e:
    logger.error("Failed to connect to RedisDB, Use internal cache dictionary for storing data.")
    _fake_db = OrderedDict()


def validate_values(latitude, longitude):
    if int(latitude) > 90 or int(latitude) < -90:
        return False
    if int(longitude) > 180 or int(longitude) < -180:
        return False
    return True


@bottle.route('/:#.*#', method='ANY')
def default_action():
    bottle.response.status = 404
    return


@bottle.get(ROOT_URL_PATH)
def list_action():
    try:
        bottle.response.status = 200
        if _fake_db is None:  # redis in use
            keys = redis_client.keys()
            vals = [json.loads(redis_client.get(x)) for x in keys if str(x).isdigit()]
            logger.debug('list all: keys: %s, vals: %s', keys, vals)
            return OrderedDict(zip(keys, vals))
        else:
            return _fake_db
    except Exception as e:
        logger.exception('Exception during handling GET ALL action')
        bottle.response.status = '500 Exception: %s during handling GET ALL action' % e.message
        return


@bottle.get(ROOT_URL_PATH + '<idx>')
def get_action(idx):
    logger.debug('GET: %s', idx)
    if _fake_db is None:  # redis in use
        val = redis_client.get(idx)
        if val:
            bottle.response.status = 200
            return json.loads(val)
        else:
            logger.error('Item with idx: %s not found from redis.', idx)
            bottle.response.status = 404
            return
    else:
        if _fake_db.get(idx):
            bottle.response.status = 200
            return _fake_db[idx]
        else:
            logger.error('Item with idx: %s not found from cache.', idx)
            bottle.response.status = 404
            return


@bottle.post(ROOT_URL_PATH)
def post_action():
    data = bottle.request.json
    logger.debug('POST: %s', data)
    if data:
        [latitude, longitude] = data['position']
        if validate_values(latitude, longitude):
            if _fake_db is None:  # redis in use
                idx = str(int(max(redis_client.keys())) + 1) if redis_client.keys() else '1'
                redis_client.set(idx, json.dumps(data))
            else:
                idx = str(int(_fake_db.keys()[-1]) + 1) if _fake_db else '1'
                _fake_db[idx] = data
            bottle.response.status = 201
            bottle.response.set_header('Location', ROOT_URL_PATH + idx)
        else:
            bottle.response.status = '400 Invalid Position data'
    else:
        logger.exception('Received Non-JSON format data')
        bottle.response.status = 415
    return data


@bottle.put(ROOT_URL_PATH + '<idx>')
def update_action(idx):
    data = bottle.request.json
    logger.debug('PUT: %s - %s', idx, data)

    if data:
        [latitude, longitude] = data['position']
        if validate_values(latitude, longitude):
            if _fake_db is None:  # redis in use
                if redis_client.get(idx):
                    redis_client.set(idx, json.dumps(data))
                    bottle.response.status = 200
                    return data
                else:
                    logger.error('Item with idx: %s not found from redis.', idx)
                    bottle.response.status = 404
            else:
                if _fake_db.get(idx):
                    _fake_db[idx] = data
                    bottle.response.status = 200
                    return data
                else:
                    logger.error('Item with idx: %s not found from cache.', idx)
                    bottle.response.status = 404
    else:
        logger.exception('Received Non-JSON format data')
        bottle.response.status = 415
    return


@bottle.delete(ROOT_URL_PATH + '<idx>')
def delete_action(idx):
    logger.debug('DELETE: %s', idx)

    if _fake_db is None:  # redis in use
        if redis_client.delete(idx):
            bottle.response.status = 204
            return
        else:
            logger.error('Item with idx: %s not found from redis.', idx)
            bottle.response.status = 404
            return
    else:
        if _fake_db.get(idx):
            del _fake_db[idx]
            bottle.response.status = 204
            return
        else:
            logger.error('Item with idx: %s not found from local cache.', idx)
            bottle.response.status = 404
            return


@bottle.delete(TEST_URL_PATH + '<delete_authentication>')
# For testing purpose only
def delete_action(delete_authentication):
    if delete_authentication == 'UnitTest_only':
        if _fake_db is None:  # redis in use
            redis_client.flushall()
        else:
            _fake_db.clear()
        bottle.response.status = 204
        return
    else:
        bottle.response.status = 400
        return 'Invalid request! Provide Delete Authentication String in order to remove all Data. FOR TESTING ONLY'


def server_start(ip, port):
    bottle.run(host=ip, port=port)


if __name__ == '__main__':
    bind_ip = '0.0.0.0'
    bind_port = 3000
    try:
        if len(sys.argv) < 2:
            logger.info('No given bind IP and port, use default value as: %s:%s', bind_ip, bind_port)
        elif len(sys.argv) == 2:
            bind_ip = sys.argv[1]
            logger.info('Override bind IP to: %s', bind_ip)
        else:
            bind_ip = sys.argv[1]
            bind_port = sys.argv[2]
            logger.info('Override bind IP and port to: %s:%s', bind_ip, bind_port)
    except:
        logger.exception('Exception during argument value handling, start with default value: %s:%s', bind_ip, bind_port)

    logger.info('Starting server with %s:%s', bind_ip, bind_port)
    server_start(bind_ip, bind_port)
